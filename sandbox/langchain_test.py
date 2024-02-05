import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

os.environ["OPENAI_API_KEY"] = "hoge"

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

template = """
# あなたは日本の弁護士です。
# 小学生でも分かる言葉を使って説明を考えてください。
    - 分かりやすい言葉を使って説明を考えてください。
        - 説明に法律用語を使わないでください。
    - 出力は多くても2文、140字です。
    - 用語の**正しい**説明を考えてください。
    - 適宜、**法令**を参照してください。
    - 同じ言葉を繰り返し使うのは避けてください。
# 引数が法律用語の場合、説明に法律用語が生まれた趣旨を書いてください。
# 以下の用語、または文の説明を考えてください。
    - 法律用語出ない場合、"法律用語ではありません"と返してください。

{legal_term}
"""

prompt = PromptTemplate(
    input_variables=["legal_term"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

print(chain("不動産売買"))
