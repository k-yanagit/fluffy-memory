from fastapi import FastAPI
from .models import SearchText, SearchResponse

app = FastAPI()

@app.post("/search/", response_model=SearchResponse)
async def search_text(search: SearchText):
    # 以下は仮のレスポンスです。

    description = f"詳細な説明: {search.word}"
    rough_description = f"簡単な説明: {search.word}"
    links = ["http://link1.com", "http://link2.com"]

    response = {
        "text": {
            "description": description,
            "rough_description": rough_description
        },
        "link": links
    }
    return response
