from .base_model import BaseLLM
from config import settings

# Delay importing langchain until runtime so Uvicorn/other processes don't
# attempt to initialize Google clients at import-time (which requires ADC).
class GeminiLLM(BaseLLM):
    def __init__(self):
        self._model = None

    def _init_model(self):
        if self._model is None:
            # The Google client library prefers Application Default Credentials
            # (set via GOOGLE_APPLICATION_CREDENTIALS or via `gcloud auth application-default login`).
            # If you have a service account json file, set the env var:
            #   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
            # LangChain's google_genai wrapper will use google.auth.default() which
            # reads the ADC. We still allow passing an API key, but ADC is preferred.
            import os

            # If no ADC and no API key, raise a helpful error
            has_adc = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None
            has_api_key = bool(settings.GOOGLE_API_KEY)
            if not (has_adc or has_api_key):
                raise EnvironmentError(
                    "Google credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON "
                    "or run `gcloud auth application-default login`, or set GOOGLE_API_KEY in environment."
                )

            from langchain.chat_models import init_chat_model

            # Prefer ADC (the google client library will pick it up automatically).
            kwargs = {
                "model_provider": settings.MODEL_PROVIDER,
            }
            if has_api_key:
                kwargs["api_key"] = settings.GOOGLE_API_KEY

            # If a service account file path is provided, build Credentials and pass
            # them into the LangChain wrapper (it forwards to google client constructors).
            sa_path = settings.GOOGLE_APPLICATION_CREDENTIALS
            if sa_path:
                try:
                    from google.oauth2 import service_account

                    creds = service_account.Credentials.from_service_account_file(sa_path)
                    kwargs["credentials"] = creds
                except Exception as e:
                    raise EnvironmentError(f"Failed to load service account credentials: {e}")

            self._model = init_chat_model(settings.MODEL_NAME, **kwargs)

    def invoke(self, prompt: str) -> str:
        self._init_model()
        return self._model.invoke(prompt)
