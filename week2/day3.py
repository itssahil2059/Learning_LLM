# Week 2 - Day 3: Conversational AI - Chatbot with Gradio

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load API keys
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# Initialize
openai = OpenAI()
MODEL = 'gpt-4.1-mini'

# Global system message - can be changed to experiment
# system_message = "You are a helpful assistant in a clothes store. \
# You should try to gently encourage the customer to try items that are on sale. \
# Hats are 60% off, and most other items are 50% off. \
# If the customer asks for shoes, you should respond that shoes are not on sale today, \
# but remind the customer to look at hats!"

### Step1: Zero-shot - basic system message with no examples

# system_message = "You are a helpful assistant in a clothes store. \
# You should try to gently encourage the customer to try items that are on sale. \
# Hats are 60% off, and most other items are 50% off. \
# If the customer asks for shoes, you should respond that shoes are not on sale today, \
# but remind the customer to look at hats! \
# Always greet the customer warmly and use their name if they provide it."


system_message = "You are a helpful assistant in a clothes store. \
You should try to gently encourage the customer to try items that are on sale. \
Hats are 60% off, and most other items are 50% off. \
If the customer asks for shoes, you should respond that shoes are not on sale today, \
but remind the customer to look at hats! \
Always greet the customer warmly and use their name if they provide it."

#─────────────────────────────────────────
## STEP 2: Few-shot prompting using +=
# We ADD examples to the existing message - not replace it!
# The LLM learns the exact tone and style from these examples
# ─────────────────────────────────────────

system_message += "\n\nHere are examples of ideal responses:"
system_message += """
Customer: 'What's on sale today?'
Assistant: 'Great news! Hats are 60% off and most items are 50% off - incredible deals!'

Customer: 'I need a gift for my friend'
Assistant: 'A hat makes a perfect gift - and they are 60% off right now!'

Customer: 'Do you have belts?'
Assistant: 'We don't carry belts, but our hat collection is amazing - 60% off today!'

Customer: 'Hi, I am Sarah'
Assistant: 'Welcome Sarah! So glad you are here - can I help you find something special?'
"""
system_message += "\nAlways respond in this same warm, enthusiastic, sales-focused style."


# ─────────────────────────────────────────
# Chat function with streaming + dynamic system prompt
# ─────────────────────────────────────────

def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]

    # Dynamic system prompt - adds extra context based on user message
    relevant_system_message = system_message
    if 'belt' in message.lower():
        relevant_system_message += " The store does not sell belts; \
if you are asked for belts, be sure to point out other items on sale."

    messages = [{"role": "system", "content": relevant_system_message}] \
        + history \
        + [{"role": "user", "content": message}]

    # Streaming response with yield
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response

# ─────────────────────────────────────────
# Launch Gradio ChatInterface
# ─────────────────────────────────────────

if __name__ == "__main__":
    gr.ChatInterface(fn=chat, type="messages").launch()