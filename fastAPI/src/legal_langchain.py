import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class LegalGPTChat:

    def __init__(self):
        llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0.1,)

        template = os.getenv("PROMPT")

        prompt = PromptTemplate(
            input_variables=["legal_term"],
            template=template
        )

        self.chain = LLMChain(llm=llm, prompt=prompt)

    def set_chain(self, text:str):
        return self.chain(text)
