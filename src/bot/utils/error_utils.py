ERROR_MESSAGES = {
    "network_error": "❌ Serviço indisponível. Tente novamente.",
    "user_not_found_error": "❌ Você precisa se registrar primeiro usando:\n`!registrar <aba> <coluna>`",
    "user_already_exists_error": "⚠️Você já está registrado.",
    "user_voter_not_found_error": "❌ Você precisa se registrar primeiro com:\n`!registrar <aba> <coluna>`",
    "movie_not_found_error": "❌ Filme não encontrado. Verifique o título e o ano e tente novamente.",
    "movie_details_fetch_error": "❌ Filme não encontrado. Verifique o título e o ano e tente novamente.",
    "invalid_vote_error": "❌ Voto inválido. Use um dos seguintes:\n`1 - DA HORA`\n`2 - LIXO`\n`3 - NÃO ASSISTI`",
    "spreadsheet_error": "❌ Erro ao registar na planilha",
    "column_not_found_error": "❌ Coluna não encontrada",
}

def get_error_message(code, fallback):
    return ERROR_MESSAGES.get(code, fallback)
