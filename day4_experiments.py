# Day 4 - Extra Experiments
# Tokenization deep dive + multi-turn conversation builder

import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
openai = OpenAI()
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# ── EXPERIMENT 1: Compare token counts ────────────────────────
print("=== HOW MANY TOKENS? ===")
sentences = [
    "Hi",
    "Hello my name is Sahil",
    "Artificial Intelligence is transforming the world",
    "supercalifragilisticexpialidocious",   # long word = multiple tokens
    "🎉🔥💡",                               # emojis = many tokens
]

for s in sentences:
    count = len(encoding.encode(s))
    print(f"  {count:3} tokens → '{s}'")
print()

# ── EXPERIMENT 2: Token cost estimator ────────────────────────
print("=== TOKEN COST ESTIMATOR ===")
# gpt-4o-mini pricing: $0.15 per 1M input tokens
PRICE_PER_TOKEN = 0.15 / 1_000_000

texts = {
    "Short message":     "What is AI?",
    "Medium paragraph":  "Artificial intelligence is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
    "Long conversation": "Hi I'm Sahil. " * 50,
}

for label, text in texts.items():
    token_count = len(encoding.encode(text))
    cost = token_count * PRICE_PER_TOKEN
    print(f"  {label}: {token_count} tokens → ${cost:.6f}")
print()

# ── EXPERIMENT 3: Multi-turn conversation builder ─────────────
print("=== MULTI-TURN CONVERSATION ===")

# This is exactly what ChatGPT does under the hood
conversation = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers to 1 sentence."}
]

exchanges = [
    "Hi! My name is Sahil and I study at Texas A&M Texarkana.",
    "What field am I studying?",
    "What career should I aim for?",
    "What was my name again?",
]

for user_message in exchanges:
    # add user message to history
    conversation.append({"role": "user", "content": user_message})

    # count tokens being sent each time
    full_text = " ".join([m["content"] for m in conversation])
    token_count = len(encoding.encode(full_text))

    # call API
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    reply = response.choices[0].message.content

    # add AI reply to history
    conversation.append({"role": "assistant", "content": reply})

    print(f"  User: {user_message}")
    print(f"  AI:   {reply}")
    print(f"  [tokens sent this call: {token_count}]")
    print()

print("=== KEY INSIGHT ===")
print("Notice how token count GROWS each turn.")
print("Every call sends the ENTIRE conversation.")
print("That's the memory illusion — and why long chats cost more!")