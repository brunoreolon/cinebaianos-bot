import discord

from discord.ext import commands
from discord.ui import View, Select
from discord import SelectOption

from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message
from src.bot.utils.embed_utils import EmbedUtils


class FilmeView(View):
    def __init__(self, filmes, api_client, usuario_alvo, voto, cog, timeout=10):
        super().__init__(timeout=timeout)
        self.add_item(FilmeDropdown(filmes, api_client, usuario_alvo, voto, cog))
        self.filme_selecionado = False

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if not getattr(self, "filme_selecionado", False) and hasattr(self, "message") and self.message:
            try:
                await self.message.edit(content="⏱ Tempo expirado.", view=self)
            except Exception:
                pass

class FilmeDropdown(Select):
    def __init__(self, filmes, api_client, usuario_alvo, voto, cog):
        options = [
            SelectOption(
                label=f"{filme['title']} ({filme['releaseDate'][:4]})",
                value=str(filme['id']),
                description=f"TMDb ID: {filme['id']}"
            )
            for filme in filmes
        ]
        super().__init__(placeholder="Selecione o filme a adicionar...", options=options)
        self.filmes = filmes
        self.api_client = api_client
        self.usuario_alvo = usuario_alvo
        self.voto = voto
        self.cog = cog

    async def callback(self, interaction):
        if interaction.user.id != self.usuario_alvo.id:
            await interaction.response.send_message(
                "❌ Apenas o usuário que iniciou o comando pode selecionar o filme.",
                ephemeral=True
            )
            return

        if self.view:
            self.view.filme_selecionado = True

        movie_id = int(self.values[0])
        filme = next(f for f in self.filmes if f['id'] == movie_id)

        try:
            movie = await self.cog._adicionar_filme_api(self.usuario_alvo.id, filme["id"])

            embed = EmbedUtils.filme_adicionado_embed(
                tmdb_id=movie["id"],
                responsavel=self.usuario_alvo.display_name,
                titulo=movie["title"],
                ano=movie["year"],
                genero=movie.get("genre", "Indefinido"),
                poster=movie.get("posterPath"),
                color=discord.Color(0x00ff00)
            )

            await interaction.response.send_message(embed=embed)
        except ApiError as e:
            mensagem = get_error_message(e.code, getattr(e, "detail", str(e)))
            await interaction.response.send_message(f"❌ {mensagem}", ephemeral=False)
        finally:
            self.disabled = True
            await interaction.message.edit(view=self.view)

class Filmes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="adicionar")
    async def adicionar(self, ctx, *, args=None):
        if not args:
            await ctx.send(
                "❌ Comando incorreto.\nFormato esperado:\n"
                "`!adicionar [@usuario opcional] \"Nome do Filme (ano)\" [voto opcional]`\n\n"
                "Exemplo:\n`!adicionar \"Clube da Luta (1999)\" 1`\n"
                "Ou para outro usuário:\n`!adicionar @usuario \"Clube da Luta (1999)\" 1`"
            )
            return

        if ctx.message.mentions:
            usuario_alvo = ctx.message.mentions[0]
            args = args.replace(f"<@{usuario_alvo.id}>", "").replace(f"<@!{usuario_alvo.id}>", "").strip()
        else:
            usuario_alvo = ctx.author

        try:
            resposta = await self.api_client.get(f"/users/{usuario_alvo.id}")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        VOTOS_MAPA = {1: "DA HORA", 2: "LIXO", 3: "NÃO ASSISTI"}

        partes = args.rsplit(" ", 1)
        voto = None

        if len(partes) == 2 and partes[1].isdigit():
            voto_int = int(partes[1])
            if voto_int in VOTOS_MAPA:
                voto = voto_int
                nome_com_ano = partes[0]
            else:
                await ctx.send("❌ Voto inválido. Use um dos seguintes:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`")
                return
        else:
            nome_com_ano = args

        # Extrai título e ano
        if "(" not in nome_com_ano or ")" not in nome_com_ano:
            await ctx.send("❌ Formato inválido.\nCertifique-se de escrever o nome do filme assim:\n`\"Nome do Filme (ano)\"`\n\nExemplo:\n`!adicionar \"Interestelar (2014)\" 1`")
            return

        titulo = nome_com_ano[:nome_com_ano.rfind("(")].strip()
        ano = nome_com_ano[nome_com_ano.rfind("(") + 1:nome_com_ano.rfind(")")].strip()

        payload = {
            "title": titulo,
            "year": ano,
            "chooser": {"discordId": resposta["discordId"]}
        }

        if voto:
            payload["vote"] = {"id": voto}

        # Tenta adicionar o filme
        try:
            resposta = await self.api_client.post(f"/movies/candidates", json=payload)
        except ApiError as e:
            if e.code == "multiple_movies_found" and e.options:
                filmes = e.options  # lista de filmes retornados pela API

                for filme in filmes:
                    await ctx.send(embed=EmbedUtils.criar_embed_filme_dropdown(filme))

                # 2️⃣ Cria uma única view com dropdown contendo todos os filmes
                view = FilmeView(filmes, self.api_client, usuario_alvo, voto, self, timeout=10)
                msg = await ctx.send("Escolha o filme que deseja adicionar:", view=view)
                view.message = msg  # Para poder editar depois no timeout

            else:
                await ctx.send(get_error_message(e.code, getattr(e, "detail", str(e))))

            return

        # Se apenas um filme, envia normalmente
        movie = resposta["movie"]
        embed = EmbedUtils.filme_adicionado_embed(
            tmdb_id=movie["id"],
            responsavel=usuario_alvo.display_name,
            titulo=movie["title"],
            ano=movie["year"],
            genero=movie.get("genre", "Indefinido"),
            poster=movie.get("posterPath"),
            color=discord.Color(0x00ff00)
        )

        if voto:
            embed.add_field(name="Seu voto", value=VOTOS_MAPA[voto], inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="adicionar-id")
    async def adicionar_id(self, ctx, tmdb_id: int, voto: int = None):
        usuario_alvo = ctx.author

        # Valida o voto se fornecido
        VOTOS_MAPA = {
            1: "DA HORA",
            2: "LIXO",
            3: "NÃO ASSISTI"
        }
        if voto is not None and voto not in VOTOS_MAPA:
            await ctx.send("❌ Voto inválido. Use:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`")
            return

        # Busca dados do usuário na API
        try:
            usuario = await self.api_client.get(f"/users/{usuario_alvo.id}")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        # Chama endpoint para adicionar pelo ID
        try:
            movie = await self._adicionar_filme_api(usuario_alvo.id, tmdb_id, voto)
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        # Monta embed de resposta
        embed = EmbedUtils.filme_adicionado_embed(
            tmdb_id=movie["id"],
            responsavel=usuario_alvo.display_name,
            titulo=movie["title"],
            ano=movie["year"],
            genero=movie.get("genre", "Indefinido"),
            poster=movie.get("posterPath"),
            color=discord.Color(0x00ff00)
        )

        if voto:
            embed.add_field(name="Seu voto", value=VOTOS_MAPA[voto], inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="filmes")
    async def filmes_cmd(self, ctx, *, membro: str = None):
        if membro:
            try:
                membro_obj = await commands.MemberConverter().convert(ctx, membro)
            except commands.BadArgument:
                await ctx.send("❌ Usuário inválido. Mencione um membro do servidor corretamente (ex: `@usuario`).")
                return
        else:
            membro_obj = None

        await self.listar_filmes_embed(ctx, membro_obj)

    @commands.command(name="meus-filmes")
    async def meus_filmes(self, ctx):
        await self.listar_filmes_embed(ctx, ctx.author)

    async def _adicionar_filme_api(self, discordId: str, tmdb_id: int, voto: int = None):
        payload = {
            "movie": {"id": tmdb_id},
            "chooser": {"discordId": discordId},
        }

        if voto:
            payload["vote"] = {"id": voto}

        resposta = await self.api_client.post("/movies", json=payload)

        return resposta["movie"]

    async def listar_filmes_embed(self, ctx, membro_obj=None):
        if membro_obj:
            try:
                usuario = await self.api_client.get(f"/users/{str(membro_obj.id)}")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            if not usuario:
                await ctx.send(f"{membro_obj.mention} ainda não está registrado.")
                return

            try:
                resposta = await self.api_client.get(f"/movies/users/{usuario['discordId']}")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            if not resposta:
                await ctx.send(f"{membro_obj.display_name} ainda não adicionou nenhum filme.")
                return

            # Tenta pegar o membro do servidor para usar avatar
            member = ctx.guild.get_member(membro_obj.id)
            avatar_url = member.display_avatar.url if member else None

            filmes_usuario = resposta["movies"]

            filmes_texto = ""
            for filme in filmes_usuario:
                filmes_texto += f"`{filme['id']}` - {filme['title']} ({filme['year']})\n"

            embed = EmbedUtils.lista_filmes_embed(
                responsavel=membro_obj.display_name,
                total_filmes=len(filmes_usuario),
                color=discord.Color.blurple(),
                avatar=avatar_url,
                lista_formatada=filmes_texto
            )

            await ctx.send(embed=embed)
        else:
            try:
                todos_filmes = await self.api_client.get("/movies")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            if not todos_filmes:
                await ctx.send("Nenhum filme registrado ainda.")
                return

            # Agrupa filmes por usuário
            filmes_por_usuario = {}
            for filme in todos_filmes:
                chooser = filme.get("chooser", {})
                discord_id = chooser.get("discordId", "desconhecido")
                nome = chooser.get("name", "Desconhecido")
                if discord_id not in filmes_por_usuario:
                    filmes_por_usuario[discord_id] = {
                        "name": nome,
                        "movies": []
                    }
                filmes_por_usuario[discord_id]["movies"].append(filme)

            total_geral = len(todos_filmes)

            await ctx.send(f"📊 **Total de filmes registrados:** {total_geral}")

            # Envia embed para cada usuário
            for discord_id, info in filmes_por_usuario.items():
                nome = info["name"]
                filmes_usuario = info["movies"]

                # Tenta pegar o membro do servidor para usar avatar
                member = ctx.guild.get_member(int(discord_id))
                avatar_url = member.display_avatar.url if member else None

                filmes_texto = ""
                for filme in filmes_usuario:
                    filmes_texto += f"`{filme['id']}` - {filme['title']} ({filme['year']})\n"

                embed = EmbedUtils.lista_filmes_embed(
                    responsavel=nome,
                    total_filmes=len(filmes_usuario),
                    color=discord.Color.blurple(),
                    avatar=avatar_url,
                    lista_formatada=filmes_texto
                )

                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Filmes(bot))
