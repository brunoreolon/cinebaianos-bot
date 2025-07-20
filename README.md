# 🎬 Bot de Gerenciamento de Filmes (Discord + Google Sheets + TMDb)

Este é um projeto pessoal feito entre amigos para **organizar, votar e ranquear os filmes que assistimos juntos**. Utiliza um bot do Discord integrado com uma planilha do Google Sheets e a API do TMDb para obter informações detalhadas sobre os filmes.

---

## ✅ Funcionalidades

- Adicionar filmes assistidos
- Votar se o filme foi "DA HORA", "LIXO" ou "NÃO ASSISTI" 😅😅😅
- Ver rankings e estatísticas de usuários
- Analisar gêneros mais vistos e votados
- Sincronizar dados da planilha com o banco local
- Obter link da planilha direto no Discord

---

## 💬 Comandos principais (resumo)

### 🎥 Filmes
- `!adicionar "Filme (ano)" [voto]` — Adiciona um filme
- `!filmes`, `!meus-filmes`, `!filmes @usuário` — Lista filmes

### ✅ Votação
- `!votar <linha> <voto>` — Votar (1 = DA HORA, 2 = LIXO, 3 = NÃO ASSISTI)

### 🏆 Rankings
- `!ranking` — Total de votos por usuário
- `!da-hora`, `!da-hora @usuário` — Votos DA HORA
- `!lixos`, `!lixos @usuário` — Votos LIXO

### 🎭 Gêneros
- `!generos`, `!meus-generos`, `!generos @usuário` — Gêneros mais assistidos
- `!generos-da-hora`, `!generos-lixo` — Gêneros mais votados

### 👤 Usuário
- `!registrar <aba> <coluna>` — Registrar na planilha
- `!perfil`, `!perfil @usuário` — Ver perfil
- `!usuarios` — Listar usuários

### 🔄 Sincronização
- `!sincronizar` — Atualiza banco com planilha (admin)
- `!planilha` — Mostra o link da planilha 📎

---

## 🛠️ Requisitos

- Python 3.10+
- `.env` com as chaves corretas:
  ```env
  DISCORD_TOKEN=seu_token
  GOOGLE_SHEET_ID=seu_id_da_planilha
  TMDB_API_KEY=sua_api_key
