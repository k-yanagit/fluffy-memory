from .summarizer import LegalTextProcessor

from pydantic import BaseModel
from typing import List

class SearchText(BaseModel):
    text: str
    related_text: str

    ltp = LegalTextProcessor()
    detail_return_text: str = ltp.generate_description(text)
    brief_return_text: str = ltp.process_text(text)
    links : list[str] = []
