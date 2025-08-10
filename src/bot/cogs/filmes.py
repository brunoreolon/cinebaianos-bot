import discord

from discord.ext import commands

from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message


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
            await ctx.send(get_error_message(e.code, e.message))
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
            "responsible_id": resposta["discord_id"],
            "vote": voto
        }

        try:
            resposta = await self.api_client.post(f"/movies", json=payload)
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        # Envia embed
        embed = discord.Embed(
            title=resposta["movie"]["title"],
            description=f"Ano: {resposta['movie']['year']}\nGênero: {resposta['movie']['genre'] if resposta['movie']['genre'] else 'Indefinido'}",
            color=0x00ff00
        )

        if resposta["movie"]["poster_path"]:
            embed.set_image(url=f"https://image.tmdb.org/t/p/original{resposta["movie"]["poster_path"]}")

        voto_texto = VOTOS_MAPA.get(voto) if voto else None

        if voto:
            embed.add_field(name="Seu voto", value=voto_texto, inline=False)

        linha = resposta["movie"]["spreadsheet_row"]
        id_filme = resposta["movie"]["id"]

        embed.set_footer(text=f"Responsável: {usuario_alvo.display_name}\nLinha na planilha: {linha}\nID do Filme: {id_filme}")
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
            try:
                usuario = await self.api_client.get(f"/users/{str(membro_obj.id)}")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            if not usuario:
                await ctx.send(f"{membro_obj.mention} ainda não está registrado.")
                return

            try:
                filmes = await self.api_client.get("/movies", params={"discord_id": usuario["discord_id"]})
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            if not filmes:
                await ctx.send(f"{membro_obj.display_name} ainda não adicionou nenhum filme.")
                return

            msg = f"🎬 **Filmes adicionados por {membro_obj.display_name}:**\n\n"
            filmes_usuario = filmes["movies"]
            for filme in filmes_usuario:
                msg += f"`{filme['id']}` - {filme['title']} ({filme['year']})\n"
            await ctx.send(msg)
        else:
            try:
                todos_filmes = await self.api_client.get("/movies")
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.message))
                return

            if not todos_filmes:
                await ctx.send("Nenhum filme registrado ainda.")
                return

            msg = "📽️ **Filmes adicionados:**\n"
            for usuario_filmes in todos_filmes:
                usuario = usuario_filmes["user"]
                filmes_usuario  = usuario_filmes["movies"]

                nome = usuario["name"] if usuario["name"] else "Desconhecido"
                msg += f"\n👤 **{nome}:**\n"

                for filme in filmes_usuario:
                    msg += f"`{filme['id']}` - {filme['title']} ({filme['year']})\n"

            await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Filmes(bot))
