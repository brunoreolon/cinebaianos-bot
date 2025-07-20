# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from db import criar_tabelas, registrar_usuario, buscar_usuario, registrar_voto, adicionar_filme, buscar_filmes_por_usuario, buscar_todos_os_filmes, buscar_todos_os_usuarios, contar_votos_recebidos_todos_usuario, contar_todos_os_votos_por_usuario, contar_generos_mais_assistidos, contar_generos_da_hora, contar_generos_lixo, contar_generos_por_usuario, buscar_filme_por_id
from tmdb import buscar_detalhes_filme
from sheets import adicionar_filme_na_planilha, escrever_voto_na_planilha
from sincronizar_filmes import sincronizar_planilha

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Cria as tabelas ao iniciar
criar_tabelas()

@bot.command(name="comandos")
async def comandos(ctx):
    mensagem = (
        "**📜 Lista de Comandos Disponíveis:**\n\n"
        "**🎥 Filmes:**\n"
        "• `!adicionar \"Nome do Filme (ano)\" [voto opcional]` — Adiciona um filme\n"
        "• `!filmes` — Lista todos os filmes por usuário\n"
        "• `!filmes @usuário` — Lista os filmes de um usuário específico\n"
        "• `!meus-filmes` — Lista seus próprios filmes adicionados\n\n"
        
        "**✅ Votação:**\n"
        "• `!votar <linha> <voto>` — Vota em um filme (1 = DA HORA, 2 = LIXO, 3 = NÃO ASSISTI)\n\n"

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
        "• `!registrar <aba> <coluna>` — Registra sua aba e coluna na planilha\n"
        "• `!perfil` — Exibe seu perfil\n"
        "• `!perfil @usuário` — Exibe o perfil de outro usuário\n"
        "• `!usuarios` — Lista todos os usuários registrados\n\n"

        "**🔄 Sincronização:**\n"
        "• `!sincronizar` — Sincroniza os dados da planilha com o banco (admin somente)\n\n"
        
        "**📎 Outros:**\n"
        "• `!planilha` — Exibe o link da planilha de controle de filmes\n"
        "• `!github` — Mostra o link do projeto no GitHub\n\n"
    )
    await ctx.send(mensagem)

# Comando !registrar
@bot.command(name="registrar")
async def registrar(ctx, *args):
    if len(args) < 2:
        await ctx.send("❌ Uso incorreto. Use: `!registrar <aba> <coluna>`")
        return

    aba = " ".join(args[:-1])  # Tudo menos o último é a aba
    coluna = args[-1]
    
    discord_id = str(ctx.author.id)
    nome = ctx.author.display_name

    # if buscar_usuario(discord_id):
    #     await ctx.send(f"{ctx.author.mention} você já está registrado.")
    # else:
    registrar_usuario(discord_id, nome, aba, coluna)
    await ctx.send(f"✅ {ctx.author.mention} registrado com sucesso!\n🗂️ Aba: **{aba}** | 📊 Coluna: **{coluna}**")

# Comando !perfil
@bot.command(name="perfil")
async def perfil(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    usuario = buscar_usuario(str(membro.id))

    if usuario:
        _, nome, aba, coluna = usuario
        await ctx.send(f"\n**Perfil de {membro.display_name}**\n🌐 Nome: `{nome}`\n🗂️ Aba: `{aba}`\n📊 Coluna: `{coluna}`")
    else:
        await ctx.send(f"{membro.mention} ainda não está registrado. Use `!registrar <aba> <coluna>`.")

  # Relevanta erros inesperados para não esconder bugs reais


@bot.command(name="usuarios")
async def listar_usuarios(ctx, *args):
    if args:
        await ctx.send("❌ Uso incorreto. O comando `!usuarios` não aceita argumentos.")
        return
    
    usuarios = buscar_todos_os_usuarios()
    
    if not usuarios:
        await ctx.send("Nenhum usuário registrado.")
        return

    msg = "**👥 Usuários Registrados:**\n"
    for discord_id, nome, aba, coluna in usuarios:
        mention = f"<@{discord_id}>"
        msg += f"• {mention} — `{nome}` | Aba: `{aba}`, Coluna: `{coluna}`\n"
    
    await ctx.send(msg)


@bot.command(name="adicionar")
async def adicionar(ctx, *, args=None):
    usuario = buscar_usuario(str(ctx.author.id))
    if not usuario:
        await ctx.send("❌ Você precisa se registrar primeiro usando:\n`!registrar <aba> <coluna>`")
        return

    if not args:
            await ctx.send("❌ Comando incorreto.\nFormato esperado:\n`!adicionar \"Nome do Filme (ano)\" [voto opcional]`\n\nExemplo:\n`!adicionar \"Clube da Luta (1999)\" 1`")
            return

    partes = args.rsplit(" ", 1)
    voto = None

    VOTOS_MAPA = {
        1: "DA HORA",
        2: "LIXO",
        3: "NÃO ASSISTI"
    }

    # Verifica se último argumento é um número de voto
    if len(partes) == 2:
        nome_com_ano, voto_str = partes
        if voto_str.isdigit():
            voto = int(voto_str)
            if voto not in VOTOS_MAPA:
                await ctx.send("⚠️ Voto inválido. Use um dos seguintes:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`")
                return
        else:
            await ctx.send("⚠️ O segundo parâmetro deve ser um número (1, 2 ou 3) representando seu voto.\nExemplo: `!adicionar \"Filme (2020)\" 1`")
            return
    else:
        nome_com_ano = args

    # Extrai título e ano
    if "(" not in nome_com_ano or ")" not in nome_com_ano:
        await ctx.send("❌ Formato inválido.\nCertifique-se de escrever o nome do filme assim:\n`\"Nome do Filme (ano)\"`\n\nExemplo:\n`!adicionar \"Interestelar (2014)\" 1`")
        return

    titulo = nome_com_ano[:nome_com_ano.rfind("(")].strip()
    ano = nome_com_ano[nome_com_ano.rfind("(") + 1:nome_com_ano.rfind(")")].strip()

    filme = buscar_detalhes_filme(titulo, ano)
    if not filme:
        await ctx.send("❌ Filme não encontrado. Verifique o título e o ano e tente novamente.")
        return

    voto_texto = VOTOS_MAPA.get(voto) if voto else None

    # Salva na planilha
    linha = adicionar_filme_na_planilha(
        titulo=filme.title,
        aba=usuario[2],
        coluna=usuario[3],
        voto=voto_texto
    )

    # Salva no banco
    id_filme = adicionar_filme(
        titulo=filme.title,
        id_responsavel=usuario[0],
        linha_planilha=linha,
        genero=filme.genres[0]["name"] if filme.genres else "Indefinido",
        ano=filme.ano,
        tmdb_id=filme.id
    )

    if voto:
        registrar_voto(id_filme=id_filme, id_responsavel=usuario[0], id_votante=usuario[0], voto=voto_texto)

    # Envia embed
    embed = discord.Embed(
    title=filme.title,
        description=f"Ano: {filme.ano}\nGênero: {filme.genres[0]['name'] if filme.genres else 'Indefinido'}",
        color=0x00ff00
    )
    
    if filme.poster_path:
        embed.set_image(url=f"https://image.tmdb.org/t/p/original{filme.poster_path}")

    if voto:
        embed.add_field(name="Seu voto", value=voto_texto, inline=False)

    embed.set_footer(text=f"ID na planilha: {linha}\nID do Filme: {id_filme}")
    await ctx.send(embed=embed)

@bot.command(name="votar")
async def votar(ctx, id_filme: int = None, voto: int = None):
    usuario_votante = buscar_usuario(str(ctx.author.id))
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

    filme = buscar_filme_por_id(id_filme)

    if not filme:
        await ctx.send("⚠️ Filme não encontrado no banco. Ele pode ter sido adicionado manualmente ou fora do sistema.")
        return

    id_filme = filme[0]
    id_responsavel = filme[2]
    id_linha = filme[3]

    usario_responsavel_filme = buscar_usuario(id_responsavel)
    aba_responsavel = usario_responsavel_filme[2]

    sucesso = escrever_voto_na_planilha(aba_responsavel, id_linha, coluna_votante, voto_texto)
    if not sucesso:
        await ctx.send("❌ Erro ao registrar o voto na planilha. Verifique se o ID da linha e a aba estão corretos.")
        return

    registrar_voto(id_filme=id_filme, id_responsavel=id_responsavel, id_votante=id_votante, voto=voto_texto)
    await ctx.send(f"✅ Voto registrado com sucesso!\nAba: {aba_responsavel}\n🎬 Filme: `{filme[1]}`\n🗳️ Voto: **{voto_texto}**")

@bot.command(name="filmes")
async def filmes_cmd(ctx, *, membro: str = None):
    if membro:
        try:
            membro_obj = await commands.MemberConverter().convert(ctx, membro)
        except commands.BadArgument:
            await ctx.send("❌ Usuário inválido. Mencione um membro do servidor corretamente (ex: `@usuario`).")
            return
    else:
        membro_obj = None

    await listar_filmes_embed(ctx, membro_obj)

@bot.command(name="meus-filmes")
async def meus_filmes(ctx):
    await listar_filmes_embed(ctx, ctx.author)

async def listar_filmes_embed(ctx, membro_obj=None):
    if membro_obj:
        usuario = buscar_usuario(str(membro_obj.id))
        if not usuario:
            await ctx.send(f"{membro_obj.mention} ainda não está registrado.")
            return

        filmes = buscar_filmes_por_usuario(usuario[0])
        if not filmes:
            await ctx.send(f"{membro_obj.display_name} ainda não adicionou nenhum filme.")
            return

        msg = f"🎬 **Filmes adicionados por {membro_obj.display_name}:**\n"
        for filme in filmes:
            msg += f"`{filme[0]}` - {filme[1]} ({filme[5]})\n"
        await ctx.send(msg)
    else:
        todos_filmes = buscar_todos_os_filmes()
        if not todos_filmes:
            await ctx.send("Nenhum filme registrado ainda.")
            return

        filmes_por_usuario = {}
        for filme in todos_filmes:
            id_responsavel = filme[2]
            if id_responsavel not in filmes_por_usuario:
                filmes_por_usuario[id_responsavel] = []
            filmes_por_usuario[id_responsavel].append(filme)

        msg = "📽️ **Filmes adicionados:**\n"
        for id_user, filmes in filmes_por_usuario.items():
            usuario = buscar_usuario(id_user)
            nome = usuario[1] if usuario else "Desconhecido"
            msg += f"\n👤 **{nome}:**\n"
            for filme in filmes:
                msg += f"`{filme[0]}` - {filme[1]} ({filme[5]})\n"

        await ctx.send(msg)

@bot.command(name="ranking")
async def ranking(ctx):
    ranking = contar_todos_os_votos_por_usuario()

    if not ranking:
        await ctx.send("Nenhum voto registrado ainda.")
        return

    msg = "**📊 Ranking Geral:**\n"
    for nome, da_hora, lixo in ranking:
        msg += f"• **{nome}** — 🏆 DA HORA: `{da_hora}` | 🗑️ LIXO: `{lixo}`\n"

    await ctx.send(msg)

@bot.command(name="da-hora")
async def da_hora(ctx, *, argumento: str = None):
    voto_tipo = "DA HORA"

    # Se passou argumento, tenta interpretar como menção
    if argumento:
        try:
            membro = await commands.MemberConverter().convert(ctx, argumento)
        except commands.BadArgument:
            await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
            return

        usuario = buscar_usuario(str(membro.id))
        if not usuario:
            await ctx.send(f"{membro.mention} ainda não está registrado.")
            return

        total = contar_votos_recebidos_todos_usuario(str(membro.id), voto_tipo)
        await ctx.send(f"🏆 {membro.display_name} recebeu **{total}** votos *DA HORA*.")
        return

    # Sem argumento: ranking completo
    usuarios = buscar_todos_os_usuarios()
    if not usuarios:
        await ctx.send("Nenhum usuário registrado ainda.")
        return

    ranking = []
    for discord_id, nome, _, _ in usuarios:
        total = contar_votos_recebidos_todos_usuario(discord_id, voto_tipo)
        ranking.append((nome, total))

    # Ordenar por quantidade de votos decrescente
    ranking.sort(key=lambda x: x[1], reverse=True)

    msg = "**🏆 Ranking — Top DA HORA:**\n"
    for i, (nome, total) in enumerate(ranking, 1):
        msg += f"{i}. **{nome}** — {total} votos\n"
    await ctx.send(msg)

@bot.command(name="lixos")
async def lixos(ctx, *, argumento: str = None):
    voto_tipo = "LIXO"

    if argumento:
        try:
            membro = await commands.MemberConverter().convert(ctx, argumento)
        except commands.BadArgument:
            await ctx.send("❌ Argumento inválido. Use uma menção ao usuário (`@usuário`) ou deixe vazio para ver o ranking.")
            return

        usuario = buscar_usuario(str(membro.id))
        if not usuario:
            await ctx.send(f"{membro.mention} ainda não está registrado.")
            return

        total = contar_votos_recebidos_todos_usuario(str(membro.id), voto_tipo)
        await ctx.send(f"🗑️ {membro.display_name} recebeu **{total}** votos *LIXO*.")
        return

    usuarios = buscar_todos_os_usuarios()
    if not usuarios:
        await ctx.send("Nenhum usuário registrado ainda.")
        return

    ranking = []
    for discord_id, nome, _, _ in usuarios:
        total = contar_votos_recebidos_todos_usuario(discord_id, voto_tipo)
        ranking.append((nome, total))

    ranking.sort(key=lambda x: x[1], reverse=True)

    msg = "**🗑️ Ranking — Top Lixos:**\n"
    for i, (nome, total) in enumerate(ranking, 1):
        msg += f"{i}. **{nome}** — {total} votos\n"
    await ctx.send(msg)

@bot.command(name="generos")
async def generos(ctx, membro: discord.Member = None):
    if membro:
        usuario = buscar_usuario(str(membro.id))
        if not usuario:
            await ctx.send(f"{membro.mention} ainda não está registrado.")
            return
        generos_ordenados = contar_generos_por_usuario(usuario[0])
        if not generos_ordenados:
            await ctx.send(f"{membro.display_name} ainda não adicionou filmes com gêneros.")
            return
        titulo = f"🎬 Gêneros trazidos por {membro.display_name}"
    else:
        generos_ordenados = contar_generos_mais_assistidos()
        if not generos_ordenados:
            await ctx.send("Nenhum filme registrado.")
            return
        titulo = "🎞️ Gêneros mais assistidos"

    mensagem = f"**{titulo}:**\n"
    for genero, contagem in generos_ordenados:
        mensagem += f"• {genero}: {contagem} filmes\n"

    await ctx.send(mensagem)

@bot.command(name="meus-generos")
async def meus_generos(ctx):
    usuario = buscar_usuario(str(ctx.author.id))
    if not usuario:
        await ctx.send("Você precisa se registrar primeiro com `!registrar <aba> <coluna>`.")
        return

    generos_ordenados = contar_generos_por_usuario(usuario[0])
    if not generos_ordenados:
        await ctx.send("Você ainda não adicionou filmes com gêneros.")
        return

    mensagem = "**🎬 Seus gêneros mais frequentes:**\n"
    for genero, contagem in generos_ordenados:
        mensagem += f"• {genero}: {contagem} filmes\n"

    await ctx.send(mensagem)


@bot.command(name="generos-da-hora")
async def generos_da_hora(ctx):
    generos_ordenados = contar_generos_da_hora()

    if not generos_ordenados:
        await ctx.send("Nenhum voto DA HORA registrado.")
        return

    mensagem = "**🔥 Gêneros com mais votos DA HORA:**\n"
    for genero, contagem in generos_ordenados:
        mensagem += f"• {genero}: {contagem} votos\n"

    await ctx.send(mensagem)

@bot.command(name="generos-lixo")
async def generos_lixo(ctx):
    generos_ordenados = contar_generos_lixo()

    if not generos_ordenados:
        await ctx.send("Nenhum voto LIXO registrado.")
        return

    mensagem = "**🗑️ Gêneros com mais votos LIXO:**\n"
    for genero, contagem in generos_ordenados:
        mensagem += f"• {genero}: {contagem} votos\n"

    await ctx.send(mensagem)

@bot.command(name="planilha")
async def planilha(ctx):
    await ctx.send("📄 Aqui está o link da planilha de filmes:\n"
                   "🔗 https://docs.google.com/spreadsheets/d/1PWZWjoitXowKcvEfY1ULjBcufDhF46AXivVLUuDHt4Q/edit?usp=sharing")


@bot.command(name='sincronizar')
@commands.has_permissions(administrator=True)
async def sincronizar(ctx):
    await ctx.send("🔄 Iniciando **sincronização** com a planilha... Isso pode levar alguns segundos.")

    try:
        await ctx.send("📥 Lendo filmes e atualizando banco de dados...")
        total_filmes, total_votos = sincronizar_planilha()
        
        await ctx.send(
            f"✅ **Sincronização concluída com sucesso!**\n\n"
            f"🎬 Filmes sincronizados: **{total_filmes}**\n"
            f"🗳️ Votos registrados: **{total_votos}**"
        )
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro durante a sincronização:\n```{str(e)}```")

@bot.command(name='github')
async def github(ctx):
    await ctx.send("🧠 Código-fonte disponível no GitHub:\nhttps://github.com/brunoreolon/bot-discord-cinebaianos")

def membro_valido(arg):
    return isinstance(arg, discord.Member)

@perfil.error
async def perfil_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("❌ Usuário não encontrado. Use: `!perfil [@usuário]` ou apenas `!perfil` para ver o seu.")
    else:
        raise error
    
@sincronizar.error
async def sincronizar_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando. Apenas administradores podem sincronizar a planilha.")
    else:
        raise error
    
@bot.event
async def on_command_error(ctx, error):
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

@bot.event
async def on_ready():
    logging.info(f"✅ Bot conectado como {bot.user}")

bot.run(TOKEN)
