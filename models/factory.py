import os
from config import settings

# Factory returns a singleton LLM instance. Use MOCK_LLM=1 to force mock.
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    use_mock = os.getenv("MOCK_LLM", "0") == "1"
    if use_mock:
        from .mock_model import MockLLM

        _llm_instance = MockLLM()
        return _llm_instance

    provider = settings.MODEL_PROVIDER.lower()
    if provider == "google_genai" or provider.startswith("gemini"):
        from .gemini_model import GeminiLLM

        _llm_instance = GeminiLLM()
    else:
        # default to Gemini
        from .gemini_model import GeminiLLM

        _llm_instance = GeminiLLM()

    return _llm_instance
