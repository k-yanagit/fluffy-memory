from fastapi import FastAPI
from .models import SearchText, SearchResponse

app = FastAPI()

@app.post("/search/", response_model=SearchResponse)
async def search_text(search: SearchText):
    # 以下は仮のレスポンスです。

    description = f"detail explain: {search.detail_return_text}"
    rough_description = f"brief explain: {search.brief_return_text}"
    links = search.links

    response = {
        "text": {
            "description": description,
            "rough_description": rough_description
        },
        "link": links
    }
    return response
