from pydantic import BaseModel
from typing import List

class SearchText(BaseModel):
    word: str
    text: str
    related_text: str

class ResponseText(BaseModel):
    description: str
    rough_description: str

class SearchResponse(BaseModel):
    text: ResponseText
    link: List[str]
