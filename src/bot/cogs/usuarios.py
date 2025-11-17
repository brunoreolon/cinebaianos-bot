import discord

from discord.ext import commands
from discord import Embed
from datetime import datetime

from src.bot.utils.date_utils import DateUtils
from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message

class Usuarios(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="registrar")
    async def registrar(self, ctx, *args):
        if len(args) < 1:
            await ctx.send("❌ Uso incorreto. Use: `!registrar [email]`")
            return

        discord_id = str(ctx.author.id)
        nome = ctx.author.display_name
        email = args[0]
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else None

        payload = {
            "discordId": discord_id,
            "name": nome,
            "email": email,
            "avatar": avatar_url
        }

        try:
            resposta = await self.api_client.post("/users", json=payload)
        except ApiError as e:
            await ctx.send(f"{ctx.author.mention} " + get_error_message(e.code, e.detail))
            return

        embed = Embed(
            title="🎉 Usuário Registrado com Sucesso!",
            color=0x2ecc71
        )

        embed.set_thumbnail(url=avatar_url)

        embed.add_field(
            name="👤 Nome",
            value=f"**{nome}**",
            inline=False
        )

        embed.add_field(
            name="📧 Email",
            value=f"**{resposta['email']}**",
            inline=False
        )

        embed.add_field(
            name="🆔 Discord ID",
            value=f"`{discord_id}`",
            inline=False
        )

        data_formatada = DateUtils.iso_to_br_date(resposta["joined"])

        embed.set_footer(
            text=f"Registrado em {data_formatada}"
        )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=avatar_url
        )

        await ctx.send(content=f"{ctx.author.mention}", embed=embed)


    @commands.command(name="perfil")
    async def perfil(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author

        try:
            usuario = await self.api_client.get(f"/users/{str(membro.id)}")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if usuario:
            discord_id = str(usuario["discordId"])
            nome = usuario["name"]
            email = usuario["email"]
            avatar_url = membro.display_avatar.url
            data_formatada = DateUtils.iso_to_br_date(usuario["joined"])

            embed = Embed(
                title=f"📄 Perfil de {membro.display_name}",
                color=0x3498db
            )

            embed.set_thumbnail(url=avatar_url)

            embed.add_field(
                name="👤 Nome",
                value=f"**{nome}**",
                inline=False
            )

            embed.add_field(
                name="📧 Email",
                value=f"**{email}**",
                inline=False
            )

            embed.add_field(
                name="🆔 Discord ID",
                value=f"`{discord_id}`",
                inline=False
            )

            embed.add_field(
                name="📅 Membro desde",
                value=f"{data_formatada}",
                inline=False
            )

            embed.set_footer(
                text=f"Informações atualizadas em {DateUtils.now_br_format()}"
            )

            embed.set_author(
                name=membro.display_name,
                icon_url=avatar_url
            )

            await ctx.send(content=f"{membro.mention}", embed=embed)
        else:
            await ctx.send(f"{membro.mention} ainda não está registrado. Use `!registrar [aba] [coluna]`.")

    @commands.command(name="usuarios")
    async def listar_usuarios(self, ctx, *args):
        if args:
            await ctx.send("❌ Uso incorreto. O comando `!usuarios` não aceita argumentos.")
            return

        try:
            usuarios = await self.api_client.get(f"/users")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not usuarios:
            await ctx.send("Nenhum usuário registrado.")
            return

        for usuario in usuarios:
            nome = usuario["name"]
            email = usuario.get("email", "Não informado")
            discord_id = usuario["discordId"]
            membro = ctx.guild.get_member(int(discord_id))
            avatar_url = membro.display_avatar.url if membro else None
            data_formatada = DateUtils.iso_to_br_date(usuario["joined"])

            # Menção funcional vai no content
            mention_text = f"{membro.mention}" if membro else nome

            # --- Embed compacto ---
            embed = Embed(
                title=nome,  # só o nome no título
                description=f"👤 **Nome:** {nome}\n📧 **Email:** {email}\n📅 Membro desde: {data_formatada}",
                color=0x8e44ad
            )

            if avatar_url:
                embed.set_thumbnail(url=avatar_url)

            embed.set_footer(text=f"Listagem gerada em {DateUtils.now_br_format()}")

            await ctx.send(content=mention_text, embed=embed)

async def setup(bot):
    await bot.add_cog(Usuarios(bot))