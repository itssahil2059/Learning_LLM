# Day 2: Using OpenAI Python Client with Multiple Providers
# Comparing responses from different models

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain LLMs in one sentence"}]
)
print("GPT:", response.choices[0].message.content)