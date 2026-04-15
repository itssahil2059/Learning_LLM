# Week 2 - Day 4: FlightAI - Tool Calling with SQLite
# Following Ed Donner's LLM Engineering Course
# Key concept: Giving LLMs the ability to call real functions

import os
import json
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
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
"""

# ─────────────────────────────────────────
# SQLite Database Setup
# Store ticket prices permanently on disk
# ─────────────────────────────────────────

with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)')
    conn.commit()

# Seed initial prices
ticket_prices = {"london": 799, "paris": 899, "tokyo": 1420, "sydney": 2999}
for city, price in ticket_prices.items():
    with sqlite3.connect(DB) as conn:
        conn.cursor().execute(
            'INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?',
            (city, price, price)
        )
        conn.commit()

# ─────────────────────────────────────────
# Tool Functions
# These are real Python functions the LLM can request
# ─────────────────────────────────────────

def get_ticket_price(city):
    """Look up ticket price from database"""
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
        result = cursor.fetchone()
        return f"Ticket price to {city} is ${result[0]}" if result else "No price data available"

def set_ticket_price(city, price):
    """Set or update a ticket price in the database"""
    print(f"DATABASE TOOL CALLED: Setting price for {city} to ${price}", flush=True)
    with sqlite3.connect(DB) as conn:
        conn.cursor().execute(
            'INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?',
            (city.lower(), price, price)
        )
        conn.commit()
    return f"Price for {city} has been set to ${price}"

# ─────────────────────────────────────────
# Tool Schemas
# Describe functions to the LLM in JSON format
# The LLM reads these descriptions to decide which tool to call
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

set_price_function = {
    "name": "set_ticket_price",
    "description": "Set or update the ticket price for a destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city to set the price for",
            },
            "price": {
                "type": "number",
                "description": "The new ticket price in USD",
            },
        },
        "required": ["destination_city", "price"],
        "additionalProperties": False
    }
}

# Both tools in one list
tools = [
    {"type": "function", "function": price_function},
    {"type": "function", "function": set_price_function},
]

# ─────────────────────────────────────────
# Tool Handler
# Detects which tool the LLM requested and runs it
# ─────────────────────────────────────────

def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if tool_name == "get_ticket_price":
            city = arguments.get("destination_city")
            result = get_ticket_price(city)

        elif tool_name == "set_ticket_price":
            city = arguments.get("destination_city")
            price = arguments.get("price")
            result = set_ticket_price(city, price)

        else:
            result = "Unknown tool called"

        responses.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id
        })
    return responses

# ─────────────────────────────────────────
# Chat Function
# while loop handles chained tool calls
# ─────────────────────────────────────────

def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    # Keep looping as long as LLM wants to call tools
    while response.choices[0].finish_reason == "tool_calls":
        msg = response.choices[0].message
        tool_responses = handle_tool_calls(msg)
        messages.append(msg)
        messages.extend(tool_responses)
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    return response.choices[0].message.content

# ─────────────────────────────────────────
# Launch
# ─────────────────────────────────────────

if __name__ == "__main__":
    gr.ChatInterface(fn=chat, type="messages").launch()