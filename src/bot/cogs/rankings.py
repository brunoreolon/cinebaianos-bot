from discord.ext import commands

from src.bot.exception.api_error import ApiError
from src.bot.utils.error_utils import get_error_message


class Rankings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="ranking")
    async def ranking(self, ctx):
        try:
            resposta = await self.api_client.get(f"/votes/rankings")
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        if not resposta:
            await ctx.send("Nenhum voto registrado ainda.")
            return

        msg = "**📊 Ranking Geral:**\n"
        for usuario_votos in resposta:
            usuario = usuario_votos["user"]
            votes = usuario_votos.get("votes", [])

            votes_sorted = sorted(votes, key=lambda v: v["type"]["id"])

            # monta a parte de votos dinamicamente, com ícones
            votos_str = " | ".join(
                f"{vote['type']['emoji']} {vote['type']['description']}: `{vote.get('totalVotes', 0)}`"
                for vote in votes_sorted
            )

            msg += f"• **{usuario['name']}** — {votos_str}\n"

        await ctx.send(msg)

    @commands.command(name="da-hora")
    async def da_hora(self, ctx, *, argumento: str = None):
        type_id = 1
        icone = "🏆"
        titulo = "Top DA HORA"

        if argumento:
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            try:
                resposta = await self.api_client.get(f"/votes/users/{membro.id}", params={"type": type_id})
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            votes = resposta.get("votes", [])
            total = await self._get_total_votes_for_type(votes, type_id)
            await ctx.send(f"{icone} {membro.display_name} recebeu **{total}** votos *DA HORA*.")
            return

        # ranking completo
        try:
            resposta = await self.api_client.get(f"/votes/rankings", params={"type": type_id})
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        msg = await self._build_ranking_message(resposta, type_id, icone, titulo)
        await ctx.send(msg)

    @commands.command(name="lixos")
    async def lixos(self, ctx, *, argumento: str = None):
        type_id = 2
        icone = "🗑️"
        titulo = "Top Lixos"

        if argumento:
            try:
                membro = await commands.MemberConverter().convert(ctx, argumento)
            except commands.BadArgument:
                await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
                return

            try:
                resposta = await self.api_client.get(f"/votes/users/{membro.id}", params={"type": type_id})
            except ApiError as e:
                await ctx.send(get_error_message(e.code, e.detail))
                return

            votes = resposta.get("votes", [])
            total = await self._get_total_votes_for_type(votes, type_id)
            await ctx.send(f"{icone} {membro.display_name} recebeu **{total}** votos *LIXO*.")
            return

        try:
            resposta = await self.api_client.get(f"/votes/rankings", params={"type": type_id})
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.detail))
            return

        msg = await self._build_ranking_message(resposta, type_id, icone, titulo)
        await ctx.send(msg)

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