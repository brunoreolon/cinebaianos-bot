from discord.ext import commands

from src.bot.utils.error_utils import get_error_message
from src.bot.exception.api_error import ApiError


class Votos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_client = bot.api_client

    @commands.command(name="votar")
    async def votar(self, ctx, id_filme: int = None, voto: int = None):
        # Validação dos argumentos
        if id_filme is None or voto is None:
            await ctx.send(
                "❌ Uso incorreto do comando.\n"
                "Formato correto:\n`!votar <id_filme> <voto>`\n\n"
                "**Votos possíveis:**\n"
                "`1 - DA HORA`\n"
                "`2 - LIXO`\n"
                "`3 - NÃO ASSISTI`"
            )
            return

        VOTOS_MAPA = {
            1: "DA HORA",
            2: "LIXO",
            3: "NÃO ASSISTI"
        }

        if voto not in VOTOS_MAPA:
            await ctx.send("⚠️ Voto inválido. Use:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`")
            return

        payload = {
            "voter_id": str(ctx.author.id),
            "movie_id": id_filme,
            "vote": voto
        }

        try:
            resposta = await self.api_client.post(f"/votes", json=payload)
        except ApiError as e:
            await ctx.send(get_error_message(e.code, e.message))
            return

        # if not filme:
        #     await ctx.send("⚠️ Filme não encontrado no banco. Ele pode ter sido adicionado manualmente ou fora do sistema.")
        #     return


        # if not sucesso:
        #     await ctx.send("❌ Erro ao registrar o voto na planilha. Verifique se o ID da linha e a aba estão corretos.")
        #     return

        aba_responsavel = resposta["movie"]["responsible"]["tab"]
        filme = resposta["movie"]["title"]
        voto_texto = VOTOS_MAPA[voto]

        await ctx.send(f"✅ Voto registrado com sucesso!\n🗂️ Aba: {aba_responsavel}\n🎬 Filme: `{filme}`\n🗳️ Voto: **{voto_texto}**")

async def setup(bot):
    await bot.add_cog(Votos(bot))