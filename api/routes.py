from fastapi import APIRouter, Request
from models.factory import get_llm

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    llm = get_llm()
    response = llm.invoke(prompt)
    return {"response": response}


@router.get("/health")
async def health():
    return {"status": "ok"}
