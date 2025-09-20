from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings loaded from environment.

    Use GOOGLE_APPLICATION_CREDENTIALS (preferred) or GOOGLE_API_KEY for
    authenticating to Google Generative AI (Gemini/PaLM).
    """

    GOOGLE_API_KEY: str | None = Field(None, description="Google API key (optional, use ADC when possible)")
    MODEL_PROVIDER: str = Field("google_genai", description="Model provider string")
    MODEL_NAME: str = Field("gemini-2.5-flash", description="Model name to pass to LangChain")
    GOOGLE_APPLICATION_CREDENTIALS: str | None = Field(
        None, description="Path to a Google service account JSON file (preferred)")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def has_google_credentials(self) -> bool:
        """Return True if either ADC/service-account file or GOOGLE_API_KEY is available."""
        # Application Default Credentials are typically detected by the Google
        # client library (google.auth.default). We check common signals here.
        if self.GOOGLE_API_KEY:
            return True
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return True
        return False


settings = Settings()
