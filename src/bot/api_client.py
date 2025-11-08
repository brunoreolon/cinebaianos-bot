import logging
import aiohttp
import asyncio
from src.bot.config import Config
from src.bot.exception.api_error import ApiError


class ApiClient:
    def __init__(self, session, access_token=None, refresh_token=None):
        self.session = session
        self.access_token = access_token
        self.refresh_token = refresh_token
        self._lock = asyncio.Lock()  # evita múltiplos refresh simultâneos

    @classmethod
    async def create(cls):
        session = aiohttp.ClientSession(
            headers={"Content-Type": "application/json"}
        )
        client = cls(session)

        try:
            await client._authenticate()
        except aiohttp.ClientConnectorError:
            logging.warning(
                "⚠️ Não foi possível conectar à API no startup. "
                "O bot iniciará mesmo assim, alguns comandos podem não funcionar."
            )
        except ApiError as e:
            logging.warning(
                f"⚠️ Erro de autenticação inicial: {e.code} - {e.detail}"
            )

        return client

    async def login(self):
        """Força login na API, obtendo novos tokens."""
        await self._authenticate()
        return f"✅ Login realizado com sucesso. Token atualizado."

    async def refresh_token_manual(self):
        """Força o refresh do token de acesso usando o refresh token atual."""
        try:
            await self._refresh_token()
            return "Token atualizado com sucesso."
        except ApiError as e:
            raise e
        except Exception as e:
            raise e

    async def logout(self):
        """
        Método público que expõe o logout para comandos do bot.
        """
        return await self._logout()

    async def _logout(self):
        """
        Método interno que faz logout chamando o endpoint da API e limpando tokens.
        """
        if not self.access_token:
            return "Você já está desconectado."

        payload = {"refreshToken": self.refresh_token}

        url = f"{Config.API_BASE_URL}/auth/logout"
        try:
            async with self.session.post(url, json=payload) as resp:
                if resp.status != 204:
                    try:
                        error_data = await resp.json()
                    except Exception:
                        error_data = {}

                    logging.error(
                        "Falha ao fazer logout. Status: %s, Resposta: %s",
                        resp.status, error_data
                    )

                    raise ApiError(
                        code=error_data.get("errorCode"),
                        title=error_data.get("title"),
                        detail=error_data.get("detail"),
                        status=resp.status,
                        options=None
                    )

                # Limpa tokens locais
                self.access_token = None
                self.refresh_token = None
                self.session.headers.pop("Authorization", None)

                logging.info("✅ Logout realizado com sucesso.")
                return "Logout realizado com sucesso."

        except aiohttp.ClientError as e:
            logging.error(f"Erro de rede ao tentar logout: {e}")
            raise ApiError(
                code="network_error",
                title="Erro de rede",
                detail=str(e),
                status=500,
                options=None
            )

    async def _authenticate(self):
        logging.info("🔑 Autenticando o bot na API...")

        payload = {
            "username": Config.BOT_USERNAME,
            "password": Config.BOT_PASSWORD,
        }

        try:
            async with self.session.post(f"{Config.API_BASE_URL}/auth/login", json=payload) as resp:
                if resp.status != 200:
                    try:
                        error_data = await resp.json()
                    except Exception:
                        error_data = {}
                    raise ApiError(
                        code=error_data.get("errorCode", "auth_failed"),
                        title=error_data.get("title", "Falha na autenticação"),
                        detail=error_data.get("detail", "Erro ao autenticar"),
                        status=resp.status,
                        options=None
                    )

                data = await resp.json()
                self.access_token = data.get("accessToken")
                self.refresh_token = data.get("refreshToken")

                if not self.access_token or not self.refresh_token:
                    raise ApiError(
                        code="auth_failed",
                        title="Tokens não retornados pela API.",
                        detail="Tokens não retornados pela API.",
                        status=500,
                        options=None
                    )

                self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
                logging.info("✅ Autenticação bem-sucedida.")

        except aiohttp.ClientConnectorError:
            logging.error(
                "❌ Não foi possível conectar à API (%s). "
                "Verifique se a API está rodando.", Config.API_BASE_URL
            )
            raise ApiError(
                code="api_unavailable",
                title="API indisponível",
                detail=f"Não foi possível conectar à API ({Config.API_BASE_URL}).",
                status=503,
                options=None
            )

    async def _refresh_token(self):
        if not self.refresh_token:
            logging.warning("⚠️ Tentativa de refresh sem refresh_token — usuário provavelmente deslogado.")
        raise ApiError(
            code="bot_logged_out",
            title="Bot desconectado",
            detail="Você precisa se autenticar novamente.",
            status=401,
            options=None
        )

        async with self._lock:
            logging.info("🔄 Iniciando refresh do token...")

            payload = {"refreshToken": self.refresh_token}

            try:
                async with self.session.post(f"{Config.API_BASE_URL}/auth/refresh", json=payload) as resp:
                    if resp.status != 200:
                        error_data = await resp.json()
                        code = error_data.get("errorCode")

                        logging.error(
                            "❌ Falha ao atualizar token. Status: %s, Payload: %s, Resposta: %s",
                            resp.status, payload, error_data
                        )

                        # Se o refresh token expirou, faz login novamente automaticamente
                        if code == "expired_refresh_token":
                            logging.info("🔑 Refresh token expirado. Reautenticando...")
                            await self._authenticate()
                            return

                        raise ApiError(
                            code=code,
                            title=error_data.get("title"),
                            detail=error_data.get("detail"),
                            status=resp.status,
                            options=None
                        )

                    data = await resp.json()
                    self.access_token = data.get("accessToken")
                    self.refresh_token = data.get("refreshToken", self.refresh_token)
                    self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
                    logging.info("✅ Token atualizado com sucesso.")

            except aiohttp.ClientConnectorError:
                logging.error(
                    "❌ Não foi possível conectar à API durante refresh do token."
                )
                raise ApiError(
                    code="api_unavailable",
                    title="API indisponível",
                    detail=f"Não foi possível conectar à API ({Config.API_BASE_URL}) durante refresh do token.",
                    status=503,
                    options=None
                )

    async def _request(self, method, path, **kwargs):
        url = f"{Config.API_BASE_URL}{path}"
        logging.info(f"➡️ Request: {method} {url}")

        try:
            async with self.session.request(method, url, **kwargs) as resp:
                if resp.status == 401:
                    logging.warning("⌛ Token expirado ou inválido. Tentando refresh...")
                    await self._refresh_token()
                    # Repete a requisição original
                    async with self.session.request(method, url, **kwargs) as retry_resp:
                        return await self._handle_response(retry_resp)
                return await self._handle_response(resp)

        except aiohttp.ClientConnectorError:
            logging.error("❌ Não foi possível conectar à API (%s).", Config.API_BASE_URL)
            raise ApiError(
                code="api_unavailable",
                title="API indisponível",
                detail=f"Não foi possível conectar à API ({Config.API_BASE_URL}).",
                status=503,
                options=None
            )
        except aiohttp.ClientError as e:
            logging.error(f"Erro de rede: {e}")
            raise ApiError(
                code="network_error",
                title="Erro de rede",
                detail=str(e),
                status=500,
                options=None
            )

    async def _handle_response(self, resp):
        content = await resp.text()
        logging.debug(f"Response content: {content}")

        if resp.status >= 400:
            try:
                error_data = await resp.json()
            except Exception:
                error_data = {}

            raise ApiError(
                code=error_data.get("errorCode"),
                title=error_data.get("title"),
                detail=error_data.get("detail"),
                status=resp.status,
                options=None
            )

        try:
            return await resp.json()
        except aiohttp.ContentTypeError:
            return content

    async def get(self, path, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def close(self):
        await self.session.close()
