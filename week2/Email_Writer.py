# Week 2 - Mini Project: AI Email Writer

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
openai = OpenAI()

def write_email(topic, tone):
    """Generate professional email"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write clear, professional emails.",
            },
            {
                "role": "user",
                "content": f"Write an email about '{topic}' in a '{tone}' tone.",
            },
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    pass  # TODO: add UI
