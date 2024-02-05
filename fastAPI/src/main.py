from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from legal_gpt_chat import LegalGPTChat # あなたのクラスをインポート

app = FastAPI()
legal_gpt_chat = LegalGPTChat()

class LegalTerm(BaseModel):
    text: str

@app.post("/chat/")
async def chat(legal_term: LegalTerm):
    try:
        response = legal_gpt_chat.chat_text_to_json(legal_term.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

