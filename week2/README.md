# 🤖 Week 2 - Multi-Provider LLM Clients & Chatbot

# Day1 
## What I Learned
- How to connect to 6 different AI providers using one unified OpenAI client
- The `base_url` pattern that makes this possible
- Building a conversational chatbot with Gradio UI
- Implementing tool calling with a real project (FlightAI airline assistant)
- Multi-modal AI: text + image generation + text-to-speech

## Key Concept: One Library, Many Providers
All major AI companies copied OpenAI's API format.
So the same Python code works for everyone - just change the address:

```python
openai    = OpenAI()  # default
gemini    = OpenAI(api_key=google_key,    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
grok      = OpenAI(api_key=grok_key,      base_url="https://api.x.ai/v1")
deepseek  = OpenAI(api_key=deepseek_key,  base_url="https://api.deepseek.com")
groq      = OpenAI(api_key=groq_key,      base_url="https://api.groq.com/openai/v1")
ollama    = OpenAI(api_key="ollama",      base_url="http://localhost:11434/v1")
```

## Files
| File | Description |
|---|---|
| `day1.py` | Multi-provider client setup + API key loading |
| `day2.py` | Making API calls across providers |

## Providers Used
| Provider | Model | Cost |
|---|---|---|
| OpenAI | gpt-4.1-mini | Pay per use |
| Gemini | gemini-2.0-flash | Free tier |
| Grok | grok-3-fast | Free credits |
| DeepSeek | deepseek-chat | Very cheap |
| Groq | llama3 | Free |
| Ollama | llama3.2 | Free (local) |

## Tools & Libraries
- `openai` - Python client library
- `python-dotenv` - loading API keys from .env file
- `os` - reading environment variables

## Key Lessons
- Always put imports at the TOP of your file
- Never hardcode API keys - always use `.env` file
- Add `.env` to `.gitignore` before first commit
- Every notebook must be self-contained - don't rely on other notebooks having run first
- `os.getenv()` returns `None` if key doesn't exist - won't crash until you actually use it

# 🤖 Day2 - Multi-Provider LLM Clients & Gradio UI

## What I Learned
- Connecting to 6 AI providers using unified OpenAI client pattern
- Building web UIs with Gradio in one line of Python
- Streaming AI responses word by word using `yield`
- Multi-model support — user selects GPT or Gemini from dropdown
- Two AIs talking to each other automatically
- Password protecting Gradio apps
- Global variables and when to use them

## Key Concept: One Library, Many Providers
```python
openai   = OpenAI()
gemini   = OpenAI(api_key=google_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
grok     = OpenAI(api_key=grok_key,   base_url="https://api.x.ai/v1")
ollama   = OpenAI(api_key="ollama",   base_url="http://localhost:11434/v1")

## ✈️ Day 4 — FlightAI Tool Calling

### What I Built
A FlightAI airline customer support assistant that can look up and set real ticket prices using tool calling.

### Key Concepts Learned

**Tool Calling** — giving the LLM the ability to request real Python functions:
- LLM does NOT run code itself
- It sends a message saying "please call this function with these args"
- Your Python code runs the function and sends result back
- LLM uses result to form final answer

**The Tool Calling Loop:**
```python
while response.choices[0].finish_reason == "tool_calls":
    # run the tool
    # send result back
    # call API again
```

**Why while not if:**
- `if` handles ONE round of tool calls
- `while` handles CHAINED tool calls (LLM calls tools multiple times)

**Tool Schema** — describing functions to the LLM in JSON:
```python
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a ticket",  # LLM reads this!
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {"type": "string"}
        },
        "required": ["destination_city"]
    }
}
```

**SQLite Database** — storing prices permanently:
```python
# Read
cursor.execute('SELECT price FROM prices WHERE city = ?', (city,))

# Write
cursor.execute('INSERT INTO prices (city, price) VALUES (?, ?) 
               ON CONFLICT(city) DO UPDATE SET price = ?', (city, price, price))
```

### Files
| File | Description |
|---|---|
| `day4.py` | FlightAI chatbot with tool calling and SQLite |

### Tools Built
| Tool | What it does |
|---|---|
| `get_ticket_price` | Looks up ticket price from database |
| `set_ticket_price` | Sets or updates a ticket price |

## 🎨 Day 5 — Multi-Modal FlightAI

### What I Built
Full multi-modal airline assistant combining text chat, image generation and text-to-speech audio.

### Key Concepts

**artist()** — generates a travel image using DALL-E-3 (~4 cents per image)

**talker()** — converts AI response to spoken audio using TTS

**gr.Blocks** — custom Gradio UI with full control over layout:
- Left panel: chatbot
- Right panel: generated city image  
- Below: audio playback
- Bottom: text input

**Two-step submit pattern:**
- Step 1: put_message_in_chatbot() — adds user message to chat instantly
- Step 2: chat() — calls API, generates audio and image, updates everything

### New vs Day 4
| Day 4 | Day 5 |
|---|---|
| Text only | Text + Image + Audio |
| gr.ChatInterface | gr.Blocks (custom layout) |
| Simple chat function | Returns 3 outputs |

## 📄 Project — Resume Analyzer

### What it does
AI-powered resume analyzer that reads resumes and provides detailed feedback on:
- Overall quality score
- Key skills identified
- Experience level assessment
- Formatting suggestions
- Missing keywords for target jobs

### Technologies
- Gradio for UI
- OpenAI GPT-4 mini for analysis
- Python for backend

### Status
🚀 Project started - Core structure in place