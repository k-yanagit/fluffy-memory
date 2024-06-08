from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from legal_langchain import LegalGPTChat
import logging

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()
legal_gpt_chat = LegalGPTChat()


class LegalTerm(BaseModel):
    text: str


@app.post("/chat/")
async def chat(legal_term: LegalTerm):
    try:
        response = legal_gpt_chat.set_chain(legal_term.text)
        logger.warning(f"Response: {response}")
        return response  # FastAPI automatically converts dict to JSON
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境ではより制限的な設定を推奨します。
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
