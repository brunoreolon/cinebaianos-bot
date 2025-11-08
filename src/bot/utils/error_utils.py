ERROR_MESSAGES = {
    "network_error": "❌ Serviço indisponível. Tente novamente.",
    "invalid_or_expired_access_token": "❌ O token de acesso está inválido ou expirou. Faça login novamente.",
    "invalid_refresh_token": "❌ O token de atualização é inválido. Verifique se você está usando o token correto.",
    "expired_refresh_token": "❌ O token de atualização expirou. Solicite um novo login para obter um token válido.",
    "api_unavailable": "⚠️ Não foi possível se conectar à API agora. Por favor, tente novamente em alguns instantes.",
    "bot_logged_out": "🚪 Estou desconectado da conta. Use `!login` para me autenticar novamente.",
    "user_not_found_error": "❌ Você precisa se registrar primeiro usando:\n`!registrar <aba> <coluna>`",
    "user_already_registered": "⚠️Você já está registrado.",
    "user_voter_not_found_error": "❌ Você precisa se registrar primeiro com:\n`!registrar <aba> <coluna>`",
    "movie_not_found": "❌ Filme não encontrado.",
    "multiple_movies_found": "⚠️ Mais de um filme encontrado. Escolha o correto usando `!adicionar-id <id>`",
    "movie_already_registered": "️⚠️ Este filme já foi adicionado.",
    "vote_already_registered": "⚠️Você já votou neste filme.",
    "invalid_vote": "❌ Voto inválido. Use um dos seguintes:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`"
    # "spreadsheet_error": "❌ Erro ao registar na planilha",
    # "column_not_found_error": "❌ Coluna não encontrada"
}

def get_error_message(code, fallback):
    return ERROR_MESSAGES.get(code, fallback)
