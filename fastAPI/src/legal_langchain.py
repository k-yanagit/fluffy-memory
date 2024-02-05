import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class LegalGPTChat:

    def __init__(self):
        llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0,)

        template = """
        # あなたは日本の弁護士です。
        # 小学生でも分かる言葉を使った説明を考えてください。
            - 分かりやすい言葉を使った説明を考えてください。
            - 説明に法律用語を使わないでください。
            - 用語の**正しい**説明を考えてください。
            - 適宜、**法令**を参照してください。
            - 同じ言葉を繰り返し使うのは避けてください。
        # 書き方について
            - 出力は2文~3文、**140字以下**です。
            - 「。」で改行してください。
        # 引数が法律用語の場合、説明に法律用語が生まれた趣旨を書いてください。
        # 以下の用語、または文の説明を考えてください。
            - 法律用語出ない場合、"法律用語ではありません"と返してください。

        {legal_term}
        """

        prompt = PromptTemplate(
            input_variables=["legal_term"],
            template=template
        )

        self.chain = LLMChain(llm=llm, prompt=prompt)

    def set_chain(self, text:str):
        return self.chain(text)

print(LegalGPTChat().set_chain("著作権"))
