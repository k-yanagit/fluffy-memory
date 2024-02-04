from fastapi import FastAPI
from .models import TextToSummarize
from .summarizer.summarizer import summarize_text

app = FastAPI()

@app.post("/summarize/")
async def generate_summary(text_data: TextToSummarize):
    summary = summarize_text(text_data.text)
    return {"summary": summary}
