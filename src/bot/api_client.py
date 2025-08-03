import logging

import aiohttp

from src.bot.config import Config


class ApiClient:
    def __init__(self, session):
        self.session = session

    @classmethod
    async def create(cls):
        session = aiohttp.ClientSession(
            headers={
                "X-Bot-Token": Config.BOT_API_TOKEN,
                "Content-Type": "application/json"
            }
        )
        return cls(session)

    async def get(self, path, **kwargs):
        return await self._request("GET", path, **kwargs)

    async def post(self, path, **kwargs):
        return await self._request("POST", path, **kwargs)

    async def _request(self, method, path, **kwargs):
        from src.bot.exception.api_error import ApiError

        url = f"{Config.BASE_URL}{path}"
        logging.info(f"URL: {url}")

        try:
            async with self.session.request(method, url, **kwargs) as resp:
                content = await resp.text()
                logging.info(f"Content: {content}")

                # pega o corpo como texto, independente de JSON
                if resp.status >= 400:
                    logging.info(f"Status: {resp.status}")
                    try:
                        data = await resp.json()
                        logging.info(f"Data: {data}")
                        raise ApiError(
                            code=data.get("code", "unknown_error"),
                            message=data.get("error", "Erro desconhecido."),
                            status=resp.status
                        )
                    except aiohttp.ContentTypeError as e:
                        logging.info(f"ERRO: {e}")

                        # Mostra o conteúdo para ajudar a debugar
                        raise ApiError("unknown_error", f"Erro desconhecido. Response content: {content}", resp.status)
                return await resp.json()
        except aiohttp.ClientError as e:
            logging.info(f"ERRO2: {e}")
            raise ApiError("network_error", str(e), 500)

