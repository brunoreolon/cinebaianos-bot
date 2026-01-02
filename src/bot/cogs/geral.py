import discord
from discord import Embed
from discord.ext import commands

class Geral(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comandos")
    async def comandos(self, ctx):
        embed = discord.Embed(
            title="📜 Lista de Comandos Disponíveis",
            color=0x00ff00
        )

        # ⚙️ Admin
        embed.add_field(
            name="⚙️ Admin",
            value=(
                "`!login`            🔑 Faz login manual na API (admin somente)\n"
                "`!refresh-token`    🔄 Atualiza manualmente o token de acesso (admin somente)\n"
                "`!logout`           🚪 Faz logout do bot (admin somente)"
            ),
            inline=False
        )

        # 👤 Usuário
        embed.add_field(
            name="👤 Usuário",
            value=(
                "`!registrar [email]`       Registre sua conta (e-mail obrigatório)\n"
                "`!perfil`                  Exibe seu perfil\n"
                "`!perfil @usuário`         Exibe o perfil de outro usuário\n"
                "`!usuarios`                Lista todos os usuários registrados"
            ),
            inline=False
        )

        # 🎥 Filmes
        embed.add_field(
            name="🎥 Filmes",
            value=(
                "`!adicionar \"Nome do Filme (ano)\" [@usuário opcional]` — Adiciona um filme\n"
                "`!adicionar-id [id filme]` — Adiciona um filme pelo TMDb ID\n"
                "`!filmes` — Lista todos os filmes por usuário\n"
                "`!filmes @usuário` — Lista os filmes de um usuário específico\n"
                "`!meus-filmes` — Lista seus próprios filmes adicionados"
            ),
            inline=False
        )

        # ✅ Votação
        embed.add_field(
            name="✅ Votação",
            value=(
                "`!votar [id filme] [voto]` — Vota em um filme\n"
                "`!excluir-voto [id filme]` — Exclui seu voto em um filme\n"
                "`!opcoes-voto` — Lista os votos disponíveis"
            ),
            inline=False
        )

        # 🏆 Rankings
        embed.add_field(
            name="🏆 Rankings",
            value=(
                "`!ranking` — Quantidade total de votos DA HORA e LIXO por usuário\n"
                "`!da-hora [@usuário]` — Ranking DA HORA global ou do usuário\n"
                "`!lixos [@usuário]` — Ranking LIXO global ou do usuário"
            ),
            inline=False
        )

        # 🎭 Gêneros
        embed.add_field(
            name="🎭 Gêneros",
            value=(
                "`!generos [@usuário]` — Gêneros mais assistidos ou por usuário\n"
                "`!meus-generos` — Seus gêneros mais frequentes\n"
                "`!generos-da-hora` — Gêneros com mais votos DA HORA\n"
                "`!generos-lixo` — Gêneros com mais votos LIXO"
            ),
            inline=False
        )

        # 🔄 Sincronização
        embed.add_field(
            name="🔄 Sincronização",
            value="`!sincronizar` — ~~Sincroniza os dados da planilha com o banco (admin somente)~~ _(desativado)_",
            inline=False
        )

        # 📎 Outros
        embed.add_field(
            name="📎 Outros",
            value=(
                "`!planilha` — Exibe o link da planilha de controle de filmes\n"
                "`!github` — Mostra o link do projeto no GitHub\n"
                "`!site` — Exibe o link do site"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Geral(bot))