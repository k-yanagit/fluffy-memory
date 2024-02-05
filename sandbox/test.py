import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

assert transformers.__version__ >= "4.34.1"

model = AutoModelForCausalLM.from_pretrained("cyberagent/calm2-7b-chat-dpo-experimental", device_map="auto", torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained("cyberagent/calm2-7b-chat-dpo-experimental")
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

prompt = """
著作権についてわかりやすく説明してください。
"""

token_ids = tokenizer.encode(prompt, return_tensors="pt")
output_ids = model.generate(
    input_ids=token_ids.to(model.device),
    max_new_tokens=300,
    do_sample=True,
    temperature=0.8,
    streamer=streamer,
)
print(output_ids)
