import discord

from discord.ext import commands

class Filmes(commands.Cog):

    def __init__(self, bot, conn_provider):
        self.bot = bot

    @commands.command(name="adicionar")
    async def adicionar(self, ctx, *, args=None):
        usuario = self.usuario_repo.buscar_usuario(str(ctx.author.id))
        if not usuario:
            await ctx.send("❌ Você precisa se registrar primeiro usando:\n`!registrar <aba> <coluna>`")
            return

        if not args:
            await ctx.send("❌ Comando incorreto.\nFormato esperado:\n`!adicionar \"Nome do Filme (ano)\" [voto opcional]`\n\nExemplo:\n`!adicionar \"Clube da Luta (1999)\" 1`")
            return

        VOTOS_MAPA = {
            1: "DA HORA",
            2: "LIXO",
            3: "NÃO ASSISTI"
        }

        partes = args.rsplit(" ", 1)
        voto = None

        if len(partes) == 2 and partes[1].isdigit():
            voto_int = int(partes[1])
            if voto_int in VOTOS_MAPA:
                voto = voto_int
                nome_com_ano = partes[0]
            else:
                await ctx.send("⚠️ Voto inválido. Use um dos seguintes:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`")
                return
        else:
            nome_com_ano = args

        # Extrai título e ano
        if "(" not in nome_com_ano or ")" not in nome_com_ano:
            await ctx.send("❌ Formato inválido.\nCertifique-se de escrever o nome do filme assim:\n`\"Nome do Filme (ano)\"`\n\nExemplo:\n`!adicionar \"Interestelar (2014)\" 1`")
            return

        titulo = nome_com_ano[:nome_com_ano.rfind("(")].strip()
        ano = nome_com_ano[nome_com_ano.rfind("(") + 1:nome_com_ano.rfind(")")].strip()

        filme = buscar_detalhes_filme(titulo, ano)
        if not filme:
            await ctx.send("❌ Filme não encontrado. Verifique o título e o ano e tente novamente.")
            return

        voto_texto = VOTOS_MAPA.get(voto) if voto else None

        # Salva na planilha
        linha = adicionar_filme_na_planilha(
            titulo=filme.title,
            aba=usuario[2],
            coluna=usuario[3],
            voto=voto_texto
        )

        # Salva no banco
        id_filme = self.filme_repo.adicionar_filme(
            titulo=filme.title,
            id_responsavel=usuario[0],
            linha_planilha=linha,
            genero=filme.genres[0]["name"] if filme.genres else "Indefinido",
            ano=filme.ano,
            tmdb_id=filme.id
        )

        if voto:
            self.voto_repo.registrar_voto(id_filme=id_filme, id_responsavel=usuario[0], id_votante=usuario[0], voto=voto_texto)

        # Envia embed
        embed = discord.Embed(
            title=filme.title,
            description=f"Ano: {filme.ano}\nGênero: {filme.genres[0]['name'] if filme.genres else 'Indefinido'}",
            color=0x00ff00
        )

        if filme.poster_path:
            embed.set_image(url=f"https://image.tmdb.org/t/p/original{filme.poster_path}")

        if voto:
            embed.add_field(name="Seu voto", value=voto_texto, inline=False)

        embed.set_footer(text=f"ID na planilha: {linha}\nID do Filme: {id_filme}")
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

    async def listar_filmes_embed(self, ctx, membro_obj=None):
        if membro_obj:
            usuario = self.usuario_repo.buscar_usuario(str(membro_obj.id))
            if not usuario:
                await ctx.send(f"{membro_obj.mention} ainda não está registrado.")
                return

            filmes = self.filme_repo.buscar_filmes_por_usuario(usuario[0])
            if not filmes:
                await ctx.send(f"{membro_obj.display_name} ainda não adicionou nenhum filme.")
                return

            msg = f"🎬 **Filmes adicionados por {membro_obj.display_name}:**\n"
            for filme in filmes:
                msg += f"`{filme[0]}` - {filme[1]} ({filme[5]})\n"
            await ctx.send(msg)
        else:
            todos_filmes = self.filme_repo.buscar_todos_os_filmes()
            if not todos_filmes:
                await ctx.send("Nenhum filme registrado ainda.")
                return

            filmes_por_usuario = {}
            for filme in todos_filmes:
                id_responsavel = filme[2]
                if id_responsavel not in filmes_por_usuario:
                    filmes_por_usuario[id_responsavel] = []
                filmes_por_usuario[id_responsavel].append(filme)

            msg = "📽️ **Filmes adicionados:**\n"
            for id_user, filmes in filmes_por_usuario.items():
                usuario = self.usuario_repo.buscar_usuario(id_user)
                nome = usuario[1] if usuario else "Desconhecido"
                msg += f"\n👤 **{nome}:**\n"
                for filme in filmes:
                    msg += f"`{filme[0]}` - {filme[1]} ({filme[5]})\n"

            await ctx.send(msg)

async def setup(bot):
    conn_provider = getattr(bot, "conn_provider", None)
    await bot.add_cog(Filmes(bot, conn_provider))
