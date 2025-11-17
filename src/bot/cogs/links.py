from discord.ext import commands
from discord import Embed

from src.bot.utils.date_utils import DateUtils


class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="planilha")
    async def planilha(self, ctx):
        embed = Embed(
            title="📄 Planilha de Filmes",
            description="Aqui está o link da planilha com os filmes registrados:",
            color=0xe74c3c
        )
        # Link clicável no campo
        embed.add_field(
            name="🔗 Acessar Planilha",
            value="[Clique aqui para abrir a planilha](https://docs.google.com/spreadsheets/d/1PWZWjoitXowKcvEfY1ULjBcufDhF46AXivVLUuDHt4Q/edit?usp=sharing)",
            inline=False
        )
        embed.set_footer(text=f"Solicitado por {ctx.author.display_name} • {DateUtils.now_br_format()}")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/337/337946.png")  # ícone de planilha

        await ctx.send(embed=embed)

    @commands.command(name="github")
    async def github(self, ctx):
        embed = Embed(
            title="🧠 Código-fonte do Projeto",
            description="Os repositórios do Cinebaianos estão disponíveis abaixo:",
            color=0x95a5a6
        )

        embed.add_field(
            name="🤖 Bot Discord",
            value="[Clique aqui para acessar](https://github.com/brunoreolon/cinebaianos-bot)",
            inline=False
        )
        embed.add_field(
            name="🌐 API",
            value="[Clique aqui para acessar](https://github.com/brunoreolon/cinebaianos-api)",
            inline=False
        )
        embed.add_field(
            name="💻 Web",
            value="[Clique aqui para acessar](https://github.com/brunoreolon/cinebaianos-web)",
            inline=False
        )

        embed.set_footer(text=f"Solicitado por {ctx.author.display_name} • {DateUtils.now_br_format()}")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/25/25231.png")  # ícone GitHub

        await ctx.send(embed=embed)

    @commands.command(name="site")
    async def web(self, ctx):
        embed = Embed(
            title="🌐 Acesse a versão Web",
            description="Entre no Cinebaianos pelo navegador:",
            color=0xf1c40f
        )

        # Link clicável
        embed.add_field(
            name="🔗 Acessar Web",
            value="[Clique aqui para abrir a versão Web](https://brunoreolon.github.io/cinebaianos-web/)",
            inline=False
        )

        embed.set_footer(
            text=f"Solicitado por {ctx.author.display_name} • {DateUtils.now_br_format()}"
        )

        # Thumbnail com ícone de web
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1006/1006771.png")  # ícone de navegador

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Links(bot))