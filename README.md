# LangChain Chatbot (FastAPI)

This project is a minimal, extensible chatbot backend using FastAPI and LangChain. It supports multiple LLM providers (Google Gemini/PaLM) and is designed to be extended for MS Teams or other chat interfaces.

Quick start (PaLM / Gemini)

1. Create a Python virtualenv and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Provide credentials for PaLM (recommended):

- Create a Google service account with access to the Generative AI API and download the JSON key.
- Export the path:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/palm-service-account.json"
```

Alternatively, you can run:

```bash
gcloud auth application-default login
```

4. Start the server:

```bash
uvicorn main:app --reload
```

5. Test the chat endpoint:

```bash
curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"prompt":"Hello"}' | jq
```

Using GOOGLE_API_KEY (API key method)

If you prefer to authenticate with a Google API key instead of a service account, you can set the `GOOGLE_API_KEY` environment variable. This is less secure than using a service account and ADC, but it works for quick tests or constrained setups.

1. Export your API key:

```bash
export GOOGLE_API_KEY="your_api_key_here"
export MODEL_PROVIDER="google_genai"
export MODEL_NAME="gemini-2.5-flash"  # optional override
```

2. Start the server and call `/chat` as above:

```bash
uvicorn main:app --reload

curl -s -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
	-d '{"prompt":"Say hello from Gemini using an API key."}' | jq
```

Note: `config.py` now uses pydantic's `BaseSettings` and will load env vars from a `.env` file if present.

Notes

- For local testing without credentials, you can set `MOCK_LLM=1` to use a mock LLM, but per your request this is optional.
- To switch to Azure OpenAI later, we'll add a dedicated `azure_model.py` and extend `models/factory.py`.

