from discord.ext import commands

class Geral(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comandos")
    async def comandos(self, ctx):
        mensagem = (
            "**📜 Lista de Comandos Disponíveis:**\n\n"
            "**🎥 Filmes:**\n"
            "• `!adicionar \"Nome do Filme (ano)\" [voto opcional]` — Adiciona um filme\n"
            "• `!filmes` — Lista todos os filmes por usuário\n"
            "• `!filmes @usuário` — Lista os filmes de um usuário específico\n"
            "• `!meus-filmes` — Lista seus próprios filmes adicionados\n\n"
    
            "**✅ Votação:**\n"
            "• `!votar [id filme] [voto]` — Vota em um filme (1 = DA HORA, 2 = LIXO, 3 = NÃO ASSISTI)\n\n"
    
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
    
            "**👤 Usuário:**\n"
            "• `!registrar [aba] [coluna]` — Registra sua aba e coluna na planilha\n"
            "• `!perfil` — Exibe seu perfil\n"
            "• `!perfil @usuário` — Exibe o perfil de outro usuário\n"
            "• `!usuarios` — Lista todos os usuários registrados\n\n"

            "**🔄 Sincronização:**\n"
            "• ~~`!sincronizar` — Sincroniza os dados da planilha com o banco (admin somente)~~ _(desativado)_\n\n"

            "**📎 Outros:**\n"
            "• `!planilha` — Exibe o link da planilha de controle de filmes\n"
            "• `!github` — Mostra o link do projeto no GitHub\n\n"
        )
        await ctx.send(mensagem)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Esse comando não existe. Use `!comandos` para ver a lista de comandos.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Faltou um argumento necessário. Verifique a forma correta com `!comandos`.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ Argumento inválido. Confira se digitou corretamente.")
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Geral(bot))