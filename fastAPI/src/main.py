from fastapi import FastAPI
from .models import SearchText, SearchResponse

app = FastAPI()

@app.post("/search/", response_model=SearchResponse)
async def search_text(search: SearchText):
    # 以下は仮のレスポンスです。

    description = f"detail explain: {search.word}"
    rough_description = f"brief explain: {search.word}"
    links = ["http://link1.com", "http://link2.com"]

    response = {
        "text": {
            "description": description,
            "rough_description": rough_description
        },
        "link": links
    }
    return response
