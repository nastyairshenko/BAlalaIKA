import httpx
from .config import Cfg

class LLMClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None):
        self.api_key = api_key or Cfg.LLM_API_KEY
        self.base_url = base_url or Cfg.LLM_BASE_URL
        self.model = model or Cfg.LLM_MODEL

    async def chat(self, messages: list[dict], temperature: float = 0.6, max_tokens: int = 512) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        async with httpx.AsyncClient(timeout=40) as client:
            r = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
