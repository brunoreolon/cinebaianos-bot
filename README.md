# 🎬 Bot de Gerenciamento de Filmes (Discord + ~~Google Sheets~~ + TMDb)

Este é um projeto pessoal feito entre amigos para **organizar, votar e ranquear os filmes que assistimos juntos**. Utiliza um bot do Discord ~~-integrado com uma planilha do Google Sheets~~- e a API do TMDb para obter informações detalhadas sobre os filmes.

---

## ✅ Funcionalidades

- 🎞️ Adicionar filmes assistidos
- ✅ Votar se o filme foi "DA HORA", "LIXO" ou "NÃO ASSISTI" 😅😅😅
- 🏆 Ver rankings e estatísticas de usuários
- 🎭 Analisar gêneros mais vistos e votados
- 🔄 ~~Sincronizar dados da planilha com o banco local~~ (Desativado)
- 🔗 Obter link da planilha direto no Discord

---

## 💬 Comandos principais (resumo)

### ⚙️ ️Admin
- `!login` — Faz login manual na API
- `!refresh-token` — Atualiza manualmente o token de acesso
- `!logout` — Faz logout do bot

### 👤 Usuário
- `!registrar [email]` — Registrar a conta
- `!perfil`, `!perfil @usuário` — Ver perfil
- `!usuarios` — Listar usuários

### 🎥 Filmes
- `!adicionar "Filme (ano)"` — `!adicionar "Filme (ano)" @usuário` — Adiciona um filme
- `!adicionar-id [id filme]` — `!adicionar-id [id filme] @usuário` — Adiciona um filme pelo id do Tmdb
- `!filmes`, `!meus-filmes`, `!filmes @usuário` — Lista filmes

### ✅ Votação
- `!votar [id filme] [voto]` — Votar em um filme
- `!excluir-voto [id filme]` — Exclui seu voto em um filme
- `!opcoes-voto` — Lista os votos dísponíveis

### 🏆 Rankings
- `!ranking` — Total de votos por usuário
- `!da-hora`, `!da-hora @usuário` — Votos DA HORA
- `!lixos`, `!lixos @usuário` — Votos LIXO

### 🎭 Gêneros
- `!generos`, `!meus-generos`, `!generos @usuário` — Gêneros mais assistidos
- `!generos-da-hora`, `!generos-lixo` — Gêneros mais votados

### 🔄 Sincronização
- ~~`!sincronizar` — Atualiza banco com planilha (admin)~~ (Desativado)

### 🔗 Links:
- `!planilha` — Exibe o link da planilha
- `!github` — Exibe os links do projeto no GitHub

---

## 🛠️ Requisitos

- Python 3.10+
- `.env` com as chaves corretas:
  ```env
  DISCORD_TOKEN=
  BOT_USERNAME=
  BOT_PASSWORD=
  AUTHORIZED_DISCORD_IDS=123456789012345678,987654321098765432
  API_BASE_URL=http://localhost:8080/api
    ```
  **Nota:** `AUTHORIZED_DISCORD_IDS` deve conter os IDs do Discord autorizados a rodar comandos de admin, separados por vírgula.
