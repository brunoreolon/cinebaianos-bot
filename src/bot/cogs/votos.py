import discord
from discord.ext import commands

from src.bot.utils.error_utils import get_error_message
from src.bot.exception.api_error import ApiError


class Votos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="opcoes-voto")
    async def opcoes_voto(self, ctx):
        """
        Lista todas as opções de voto disponíveis com emoji e cor.
        """
        try:
            resposta = await self.api_client.get("/vote-types")

            if not resposta:
                await ctx.send("❌ Nenhuma opção de voto encontrada.")
                return

            # Cria embed principal
            embed = discord.Embed(
                title="🎬 Opções de Voto",
                description="Confira abaixo as opções de voto disponíveis:",
                color=discord.Color.blue()
            )

            for voto in resposta:
                voto_id = voto.get("id", "N/A")
                nome = voto.get("description", "Desconhecido")
                emoji = voto.get("emoji", "")
                cor_str = voto.get("color", "#000000")

                # Converte a cor hexadecimal para int
                try:
                    cor = int(cor_str.replace("#", ""), 16)
                except ValueError:
                    cor = 0x000000

                # Adiciona cada voto como um campo
                embed.add_field(
                    name=f"{emoji} {nome} (ID: {voto_id})",
                    value=f"Cor: `{cor_str}`",
                    inline=False
                )

            await ctx.send(embed=embed)
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))

    @commands.command(name="votar")
    async def votar(self, ctx, id_filme: int = None, voto_id: int = None):
        if id_filme is None or voto_id is None:
            await ctx.send(
                "❌ Uso incorreto do comando.\n"
                "Formato correto:\n`!votar [id_filme] [voto]`\n\n"
                "💡 Para ver os votos disponíveis, use: `!opcoes-voto`"
            )
            return

        payload = {
            "voter": {"discordId": str(ctx.author.id)},
            "movie": {"id": id_filme},
            "vote": voto_id
        }

        try:
            resposta = await self.api_client.post(f"/votes", json=payload)
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        filme = resposta["movie"]["title"]
        descricao_voto = resposta["vote"]["description"]

        await ctx.send(f"✅ Voto registrado com sucesso!\n"
                       f"🎬 Filme: `{filme}`\n"
                       f"🗳️ Voto: **{descricao_voto}**")

    @commands.command(name="votos", help="Mostra os votos de um filme pelo ID.")
    async def votos(self, ctx, id_filme: int = None):
        if id_filme is None:
            await ctx.send(
                "❌ Uso incorreto do comando.\n"
                "Formato correto:\n`!votos [id_filme]`\n\n"
            )
            return

        try:
            resposta = await self.api_client.get(f"/votes/{id_filme}/votes")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        movie = resposta["movie"]
        votes = resposta.get("votes", [])

        # 🎬 Embed principal com informações do filme
        embed_filme = discord.Embed(
            title=f"{movie['title']} ({movie['year']})",
            description=(
                f"🎭 **{movie.get('genre', 'Gênero indefinido')}**\n"
                f"👤 Escolhido por **{movie['chooser']['name']}**"
            ),
            color=discord.Color.blurple()
        )

        if movie.get("posterPath"):
            embed_filme.set_image(url=movie["posterPath"])

        embed_filme.set_footer(text=f"TMDB ID: {movie['tmdbId']} • Adicionado em {movie['dateAdded'][:10]}")

        # Envia o embed principal do filme
        await ctx.send(embed=embed_filme)

        # 🗳️ Se não há votos, informa
        if not votes:
            await ctx.send("📭 Nenhum voto registrado para este filme ainda.")
            return

        # Cria um embed individual para cada voto
        for v in votes:
            voter = v["voter"]
            vote = v["vote"]
            desc = vote["description"]
            cor = vote["color"]
            emoji = vote["emoji"]

            # Procura o membro no cache do servidor
            member = discord.utils.get(ctx.guild.members, id=int(voter["discordId"]))
            avatar_url = member.display_avatar.url if member else None

            voto_embed = discord.Embed(
                description=f"{emoji} votou **{desc.upper()}**",
                color=discord.Color(int(cor.replace("#", ""), 16))
            )

            # Coloca o avatar à esquerda do nome usando set_author
            if member:
                voto_embed.set_author(name=member.display_name, icon_url=avatar_url)
            else:
                voto_embed.set_author(name=voter["name"])  # fallback caso não encontrado

            await ctx.send(embed=voto_embed)


async def setup(bot):
    await bot.add_cog(Votos(bot))