from discord.ext import commands

class Geral(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comandos")
    async def comandos(self, ctx):
        mensagem = (
            "**📜 Lista de Comandos Disponíveis:**\n\n"
            "**⚙️ Admin:**\n"
            "• `!login` — 🔑 Faz login manual na API (admin somente)\n"
            "• `!refresh-token` — 🔄 Atualiza manualmente o token de acesso (admin somente)\n"
            "• `!logout` — 🚪 Faz logout do bot (admin somente)\n\n"

            "**👤 Usuário:**\n"
            "• `!registrar [email]` — Registre sua conta (e-mail obrigatório)\n"
            "• `!perfil` — Exibe seu perfil\n"
            "• `!perfil @usuário` — Exibe o perfil de outro usuário\n"
            "• `!usuarios` — Lista todos os usuários registrados\n\n"
            
            "**🎥 Filmes:**\n"
            "• `!adicionar \"Nome do Filme (ano)\" [voto opcional]` — Adiciona um filme\n"
            "• `!adicionar-id [id filme]` — Adiciona um filme pelo tmdb id\n"
            "• `!filmes` — Lista todos os filmes por usuário\n"
            "• `!filmes @usuário` — Lista os filmes de um usuário específico\n"
            "• `!meus-filmes` — Lista seus próprios filmes adicionados\n\n"
    
            "**✅ Votação:**\n"
            "• `!votar [id filme] [voto]` — Vota em um filme\n"
            "• `!excluir-voto [id filme]` — Exclui seu voto em um filme\n"
            "• `!opcoes-voto` — Lista os votos dísponíveis\n\n"
    
            "**🏆 Rankings:**\n"
            "• `!ranking` — Quantidade total de votos DA HORA e LIXO por usuário\n"
            "• `!da-hora` — Ranking de usuários com mais votos DA HORA\n"
            "• `!da-hora @usuário` — Total de votos DA HORA recebidos por um usuário\n"
            "• `!lixos` — Ranking de usuários com mais votos LIXO\n"
            "• `!lixos @usuário` — Total de votos LIXO recebidos por um usuário\n\n"
    
            "**🎭 Gêneros:**\n"
            "• `!generos` — Gêneros mais assistidos\n"
            "• `!generos @usuário` — Gêneros mais trazidos por um usuário\n"
            "• `!meus-generos` — Seus próprios gêneros mais frequentes\n"
            "• `!generos-da-hora` — Gêneros com mais votos DA HORA\n"
            "• `!generos-lixo` — Gêneros com mais votos LIXO\n\n"

            "**🔄 Sincronização:**\n"
            "• ~~`!sincronizar` — Sincroniza os dados da planilha com o banco (admin somente)~~ _(desativado)_\n\n"

            "**📎 Outros:**\n"
            "• `!planilha` — Exibe o link da planilha de controle de filmes\n"
            "• `!github` — Mostra o link do projeto no GitHub\n\n"
        )
        await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Geral(bot))