# Day 4 - Tokenization + Stateless Memory
# Ed Donner LLM Engineering Course

import tiktoken

# ── TOPIC 1: TOKENIZATION ──────────────────────────────────────
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

sentence = "Hi my name is Sahil and I like tiramisu cake"
tokens = encoding.encode(sentence)

print("=== TOKENIZATION ===")
print(f"Sentence: {sentence}")
print(f"Token IDs: {tokens}")
print(f"Total tokens: {len(tokens)}")
print()

print("=== TOKEN BREAKDOWN ===")
for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"  {token_id} → '{token_text}'")
print()

# ── TOPIC 2: STATELESS MEMORY ILLUSION ────────────────────────
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
openai = OpenAI()

print("=== WITHOUT HISTORY (AI forgets) ===")
messages_no_memory = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user",   "content": "What's my name?"}
]
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages_no_memory)
print(f"AI: {response.choices[0].message.content}")
print()

print("=== WITH HISTORY (AI remembers) ===")
messages_with_memory = [
    {"role": "system",    "content": "You are a helpful assistant"},
    {"role": "user",      "content": "Hi! I'm Sahil!"},
    {"role": "assistant", "content": "Hi Sahil! How can I assist you today?"},
    {"role": "user",      "content": "What's my name?"}
]
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages_with_memory)
print(f"AI: {response.choices[0].message.content}")