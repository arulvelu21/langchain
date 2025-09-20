from .base_model import BaseLLM
import os
import requests
from typing import Any


class GroqLLM(BaseLLM):
    """Minimal Groq client using HTTP so tests can run without an official SDK.

    Expected env vars:
      - GROQ_API_KEY: API key
      - GROQ_MODEL: model name (default: groq-1)
      - GROQ_API_URL: full endpoint URL to call (e.g. https://api.groq.ai/v1/models/<model>/generate)

    If the provider provides a different REST shape, adjust `invoke()` accordingly.
    """

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("GROQ_MODEL", "groq-1")
        # Allow the user to provide a full URL; otherwise we'll try a sensible default
        self.api_url = os.getenv("GROQ_API_URL", "")
        # SDK client if available
        self._sdk_client = None
        self._sdk_name = None

    def _ensure_config(self):
        if not self.api_key:
            raise EnvironmentError("GROQ_API_KEY is not set. Set it to your Groq API key to use Groq provider.")
        if not self.api_url:
            # Provide guidance rather than making a fragile default
            raise EnvironmentError(
                "GROQ_API_URL is not set. Set it to your Groq REST endpoint (for example, https://api.groq.ai/v1/models/<model>/generate)."
            )

    def invoke(self, prompt: str) -> str:
        # Try SDK first (common package names), then fall back to HTTP
        if self._sdk_client is None:
            # Try common SDK package names
            for pkg in ("groq_client", "groq", "groq_sdk"):
                try:
                    module = __import__(pkg)
                    self._sdk_client = module
                    self._sdk_name = pkg
                    break
                except Exception:
                    continue

        if self._sdk_client:
            # Attempt to call common SDK patterns. This is best-effort and may need
            # adjustment to match the real SDK's API.
            try:
                if hasattr(self._sdk_client, "GroqClient"):
                    client = self._sdk_client.GroqClient(api_key=self.api_key)
                    resp = client.generate(model=self.model, prompt=prompt)
                    # try common shapes
                    if isinstance(resp, dict) and "text" in resp:
                        return resp["text"]
                    return str(resp)
                # fallback: module may provide a top-level generate function
                if hasattr(self._sdk_client, "generate"):
                    resp = self._sdk_client.generate(model=self.model, prompt=prompt, api_key=self.api_key)
                    if isinstance(resp, dict) and "text" in resp:
                        return resp["text"]
                    return str(resp)
            except Exception as e:
                # Log the SDK error and fall back to HTTP
                import logging

                logging.getLogger(__name__).warning("Groq SDK call failed, falling back to HTTP: %s", e)

        # HTTP fallback
        self._ensure_config()

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload: dict[str, Any] = {"model": self.model, "prompt": prompt}

        try:
            resp = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
        except Exception as e:
            raise RuntimeError(f"Failed to call Groq API: {e}")

        if not resp.ok:
            raise RuntimeError(f"Groq API returned status {resp.status_code}: {resp.text}")

        data = resp.json()

        # Heuristics to extract text from common response shapes
        if isinstance(data, dict):
            for key in ("text", "output", "outputs", "choices", "generations"):
                if key in data:
                    val = data[key]
                    if isinstance(val, str):
                        return val
                    if isinstance(val, list) and val:
                        first = val[0]
                        if isinstance(first, dict) and "text" in first:
                            return first["text"]
                        return str(first)

        return str(data)
