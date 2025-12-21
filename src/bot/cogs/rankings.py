from discord.ext import commands
from discord import Embed

from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message
from src.bot.utils.date_utils import DateUtils


class Rankings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="ranking")
    async def ranking(self, ctx):
        try:
            resposta = await self.api_client.get(f"/votes/received")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not resposta:
            await ctx.send("Nenhum voto registrado ainda.")
            return

        # --- Embed principal ---
        embed = Embed(
            title="📊 Ranking Geral",
            description="Confira o desempenho dos usuários nos votos:",
            color=0xe67e22
        )

        # Ordena o ranking pelo total de votos de cada usuário (opcional)
        def total_votes(usuario_votos):
            return sum(v.get("totalVotes", 0) for v in usuario_votos.get("votes", []))

        resposta_sorted = sorted(resposta, key=total_votes, reverse=True)

        for usuario_votos in resposta_sorted:
            usuario = usuario_votos["user"]
            votes = usuario_votos.get("votes", [])

            # Ordena os votos pelo tipo id
            votes_sorted = sorted(votes, key=lambda v: v["type"]["id"])

            # Monta string de votos com emojis
            votos_str = " | ".join(
                f"{vote['type']['emoji']} {vote['type']['description']}: `{vote.get('totalVotes', 0)}`"
                for vote in votes_sorted
            ) or "Nenhum voto"

            # Adiciona cada usuário como campo
            embed.add_field(
                name=f"👤 {usuario['name']}",
                value=votos_str,
                inline=False
            )

        embed.set_footer(
            text=f"Atualizado em {DateUtils.now_br_format()}"
        )

        await ctx.send(embed=embed)

    @commands.command(name="da-hora")
    async def da_hora(self, ctx, *, argumento: str = None):
        type_id = 1
        icone = "🏆"
        titulo = "Top DA HORA"

        if argumento:
            # Mostrar apenas um usuário
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            try:
                resposta = await self.api_client.get(f"/users/{membro.id}/votes/received", params={"vote": type_id})
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            votes = resposta.get("votes", [])
            total = votes[0].get("totalVotes", 0)

            embed = Embed(
                title=f"{icone} {membro.display_name}",
                description=f"Recebeu **{total}** votos *DA HORA*",
                color=0xf1c40f
            )
            embed.set_thumbnail(url=membro.display_avatar.url)
            embed.set_footer(text=f"Consultado por {ctx.author.display_name} • {DateUtils.now_br_format()}")
            await ctx.send(embed=embed)
            return

        # Ranking completo
        try:
            resposta = await self.api_client.get(f"/votes/received", params={"type": type_id})
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not resposta:
            await ctx.send(f"Nenhum voto *DA HORA* registrado ainda.")
            return

        # --- Ordena ranking pelo total de votos ---
        def total_votes(usuario_votos):
            votes = [v for v in usuario_votos.get("votes", []) if v["type"]["id"] == type_id]
            return sum(v.get("totalVotes", 0) for v in votes)

        resposta_sorted = sorted(resposta, key=total_votes, reverse=True)

        # --- Embed principal ---
        embed = Embed(
            title=f"{icone} {titulo}",
            description="Ranking atualizado com os votos *DA HORA*:",
            color=0xf1c40f
        )

        # Medalhas e cores para Top 3
        medals = ["🥇", "🥈", "🥉"]
        colors = [0xffd700, 0xc0c0c0, 0xcd7f32]  # Ouro, prata, bronze

        for idx, usuario_votos in enumerate(resposta_sorted):
            usuario = usuario_votos["user"]
            votes = usuario_votos.get("votes", [])
            votes_type = [v for v in votes if v["type"]["id"] == type_id]
            total = sum(v.get("totalVotes", 0) for v in votes_type)

            if idx < 3:
                medal = medals[idx]
                embed.add_field(
                    name=f"{medal} {usuario['name']}",
                    value=f"{icone} **{total}** votos",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"👤 {usuario['name']}",
                    value=f"{icone} **{total}** votos",
                    inline=False
                )

        embed.set_footer(text=f"Atualizado em {DateUtils.now_br_format()}")

        await ctx.send(embed=embed)

    @commands.command(name="lixos")
    async def lixos(self, ctx, *, argumento: str = None):
        type_id = 2
        icone = "🗑️"
        titulo = "Top Lixos"

        if argumento:
            # Mostrar apenas um usuário
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            try:
                resposta = await self.api_client.get(f"/users/{membro.id}/votes/received", params={"vote": type_id})
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            votes = resposta.get("votes", [])
            total = votes[0].get("totalVotes", 0)

            embed = Embed(
                title=f"{icone} {membro.display_name}",
                description=f"Recebeu **{total}** votos *LIXO*",
                color=0x95a5a6
            )
            embed.set_thumbnail(url=membro.display_avatar.url)
            embed.set_footer(text=f"Consultado por {ctx.author.display_name} • {DateUtils.now_br_format()}")
            await ctx.send(embed=embed)
            return

        # Ranking completo
        try:
            resposta = await self.api_client.get(f"/votes/given", params={"type": type_id})
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not resposta:
            await ctx.send(f"Nenhum voto *LIXO* registrado ainda.")
            return

        # --- Ordena ranking pelo total de votos ---
        def total_votes(usuario_votos):
            votes = [v for v in usuario_votos.get("votes", []) if v["type"]["id"] == type_id]
            return sum(v.get("totalVotes", 0) for v in votes)

        resposta_sorted = sorted(resposta, key=total_votes, reverse=True)

        # --- Embed principal ---
        embed = Embed(
            title=f"{icone} {titulo}",
            description="Ranking atualizado com os votos *LIXO*:",
            color=0x95a5a6
        )

        # Medalhas e cores para Top 3
        medals = ["🥇", "🥈", "🥉"]
        colors = [0xffd700, 0xc0c0c0, 0xcd7f32]  # Ouro, prata, bronze

        for idx, usuario_votos in enumerate(resposta_sorted):
            usuario = usuario_votos["user"]
            votes = usuario_votos.get("votes", [])
            votes_type = [v for v in votes if v["type"]["id"] == type_id]
            total = sum(v.get("totalVotes", 0) for v in votes_type)

            if idx < 3:
                medal = medals[idx]
                embed.add_field(
                    name=f"{medal} {usuario['name']}",
                    value=f"{icone} **{total}** votos",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"👤 {usuario['name']}",
                    value=f"{icone} **{total}** votos",
                    inline=False
                )

        embed.set_footer(text=f"Atualizado em {DateUtils.now_br_format()}")

        await ctx.send(embed=embed)

    async def _get_total_votes_for_type(self, votes, type_id: int) -> int:
        for vote in votes:
            if vote["type"]["id"] == type_id:
                return vote.get("totalVotes", 0)
        return 0

    async def _build_ranking_message(self, resposta, type_id: int, icone: str, titulo: str) -> str:
        msg = f"**{icone} Ranking — {titulo}:**\n"
        for usuario_ranking in resposta:
            usuario = usuario_ranking["user"]
            votes = usuario_ranking.get("votes", [])
            total = await self._get_total_votes_for_type(votes, type_id)
            msg += f"**{usuario['name']}** — {total} votos\n"
        return msg

async def setup(bot):
    await bot.add_cog(Rankings(bot))