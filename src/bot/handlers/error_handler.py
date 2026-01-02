from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error') and ctx.command.on_error is not None:
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.send("🚫 Você não tem permissão para usar este comando.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Esse comando não existe. Use `!comandos` para ver a lista de comandos.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Faltou um argumento necessário. Verifique a forma correta com `!comandos`.")
        elif isinstance(error, commands.BadArgument):
            if ctx.command and ctx.command.name == "perfil":
                await ctx.send("❌ Usuário não encontrado. Use: `!perfil [@usuário]` ou apenas `!perfil` para ver o seu.")
            else:
                await ctx.send("⚠️ Argumento inválido. Confira se digitou corretamente.")

        else:
            raise error

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))