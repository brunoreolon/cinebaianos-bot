from discord.ext import commands

from src.bot.di.repository_factory import criar_filmes_repository, criar_usuarios_repository, criar_votos_repository
from src.bot.sheets.sheets import escrever_voto_na_planilha

class Votos(commands.Cog):

    def __init__(self, bot, conn_provider):
        self.bot = bot
        self.filme_repo = criar_filmes_repository(conn_provider)
        self.usuario_repo = criar_usuarios_repository(conn_provider)
        self.voto_repo = criar_votos_repository(conn_provider)

    @commands.command(name="votar")
    async def votar(self, ctx, id_filme: int = None, voto: int = None):
        usuario_votante = self.usuario_repo.buscar_usuario(str(ctx.author.id))
        if not usuario_votante:
            await ctx.send("❌ Você precisa se registrar primeiro com:\n`!registrar <aba> <coluna>`")
            return

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

        id_votante = usuario_votante[0]
        coluna_votante = usuario_votante[3]
        voto_texto = VOTOS_MAPA[voto]

        filme = self.filme_repo.buscar_filme_por_id(id_filme)

        if not filme:
            await ctx.send("⚠️ Filme não encontrado no banco. Ele pode ter sido adicionado manualmente ou fora do sistema.")
            return

        id_filme = filme[0]
        id_responsavel = filme[2]
        id_linha = filme[3]

        usario_responsavel_filme = self.usuario_repo.buscar_usuario(id_responsavel)
        aba_responsavel = usario_responsavel_filme[2]

        sucesso = escrever_voto_na_planilha(aba_responsavel, id_linha, coluna_votante, voto_texto)
        if not sucesso:
            await ctx.send("❌ Erro ao registrar o voto na planilha. Verifique se o ID da linha e a aba estão corretos.")
            return

        self.voto_repo.registrar_voto(id_filme=id_filme, id_responsavel=id_responsavel, id_votante=id_votante, voto=voto_texto)
        await ctx.send(f"✅ Voto registrado com sucesso!\n🗂️ Aba: {aba_responsavel}\n🎬 Filme: `{filme[1]}`\n🗳️ Voto: **{voto_texto}**")

async def setup(bot):
    conn_provider = getattr(bot, "conn_provider", None)
    await bot.add_cog(Votos(bot, conn_provider))