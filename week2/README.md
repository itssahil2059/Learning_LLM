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

