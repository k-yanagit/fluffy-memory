from pydantic import BaseModel

class TextToSummarize(BaseModel):
    text: str
