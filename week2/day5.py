# Week 2 - Day 5: FlightAI - Multi-Modal AI Assistant
# Following Ed Donner's LLM Engineering Course
# Key concept: Combining text + image + audio in one AI app

import os
import json
import sqlite3
import base64
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import gradio as gr

# ─────────────────────────────────────────
# Setup
# ─────────────────────────────────────────

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4.1-mini"
openai = OpenAI()
DB = "prices.db"

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
Always mention the city name when discussing ticket prices.
Wish the customer a pleasant journey when they mention booking.
"""

# ─────────────────────────────────────────
# Database
# ─────────────────────────────────────────

def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
        result = cursor.fetchone()
        return f"Ticket price to {city} is ${result[0]}" if result else "No price data available"

# ─────────────────────────────────────────
# Tool Schema
# ─────────────────────────────────────────

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]

# ─────────────────────────────────────────
# Tool Handler
# ─────────────────────────────────────────

def handle_tool_calls(message):
    responses = []
    cities = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get("destination_city")
            cities.append(city)
            result = get_ticket_price(city)
            responses.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })
    return responses, cities

# ─────────────────────────────────────────
# Multi-Modal Functions
# ─────────────────────────────────────────

def artist(city):
    """Generate a travel image for the city using DALL-E-3"""
    # Note: costs ~4 cents per image!
    image_response = openai.images.generate(
        model="dall-e-3",
        prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
        size="1024x1024",
        n=1,
        response_format="b64_json",
    )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

def talker(message):
    """Convert text response to audio using TTS"""
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="onyx",   # try: alloy, coral, onyx
        input=message
    )
    return response.content

# ─────────────────────────────────────────
# Chat Function
# Returns 3 things: history, audio, image
# ─────────────────────────────────────────

def chat(history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history

    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    cities = []
    image = None

    while response.choices[0].finish_reason == "tool_calls":
        msg = response.choices[0].message
        tool_responses, cities = handle_tool_calls(msg)
        messages.append(msg)
        messages.extend(tool_responses)
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    reply = response.choices[0].message.content
    history += [{"role": "assistant", "content": reply}]

    # Generate audio for every response
    voice = talker(reply)

    # Generate image only when a city was mentioned
    if cities:
        image = artist(cities[0])

    return history, voice, image

# ─────────────────────────────────────────
# Gradio Blocks UI
# Custom layout with chatbot + image + audio
# ─────────────────────────────────────────

def put_message_in_chatbot(message, history):
    return "", history + [{"role": "user", "content": message}]

with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500, type="messages")
        image_output = gr.Image(height=500, interactive=False)
    with gr.Row():
        audio_output = gr.Audio(autoplay=True)
    with gr.Row():
        message = gr.Textbox(label="Chat with FlightAI:")

    message.submit(
        put_message_in_chatbot,
        inputs=[message, chatbot],
        outputs=[message, chatbot]
    ).then(
        chat,
        inputs=chatbot,
        outputs=[chatbot, audio_output, image_output]
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True, auth=("flightai", "travel2025"))