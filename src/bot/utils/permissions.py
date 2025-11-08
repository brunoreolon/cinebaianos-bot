import logging
from discord.ext import commands
from src.bot.config import Config

logger = logging.getLogger(__name__)

def is_admin_or_authorized(ctx):
    """
    Retorna True se o usuário for administrador ou estiver na lista de IDs autorizados.
    Caso contrário, dispara CheckFailure.
    """
    # if ctx.author.guild_permissions.administrator or ctx.author.id in Config.AUTHORIZED_DISCORD_IDS:
    if ctx.author.id in Config.AUTHORIZED_DISCORD_IDS:
        return True
    else:
        logger.warning(f"Usuário não autorizado: {ctx.author} (ID: {ctx.author.id}) tentou usar '{ctx.command}'")
        raise commands.CheckFailure("Você não tem permissão para usar este comando.")