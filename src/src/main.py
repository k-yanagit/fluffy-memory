from fastapi import FastAPI
from .models import SearchText, SearchResponse

app = FastAPI()

@app.post("/search/", response_model=SearchResponse)
async def search_text(search: SearchText):
    # ここで、検索するワード、テキスト、関連テキストを使用して処理を行います。
    # 処理結果から説明、簡単な説明、関連リンクを生成します。
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
