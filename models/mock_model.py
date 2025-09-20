from .base_model import BaseLLM

class MockLLM(BaseLLM):
    def invoke(self, prompt: str) -> str:
        return f"[MOCK RESPONSE] You said: {prompt}"
