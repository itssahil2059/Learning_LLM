# Day 2 - LLM Engineering Building Blocks

## Key Takeaways
- Frontier models: GPT, Claude, Gemini, Grok
- Open-source LLMs: LLaMA, Mistral, DeepSeek
- OpenAI Python client can connect to multiple providers
- Ollama lets you run models locally with OpenAI-compatible endpoints

## Topics Covered
- HTTP Endpoints vs OpenAI Python Client
- Using one client library for multiple LLM providers
- Running local models with Ollama


## Frontier vs Open-Source Models

| Model | Type | Provider |
|-------|------|----------|
| GPT-4o | Frontier (Closed) | OpenAI |
| Claude | Frontier (Closed) | Anthropic |
| Gemini | Frontier (Closed) | Google |
| Grok | Frontier (Closed) | xAI |
| LLaMA | Open-Source | Meta |
| Mistral | Open-Source | Mistral AI |
| DeepSeek | Open-Source | DeepSeek |

## Key Differences
- **HTTP Endpoint:** Raw API calls using `requests` library — more control, more boilerplate
- **OpenAI Python Client:** Cleaner syntax, handles retries/errors, works with multiple providers via `base_url`
- **Ollama:** Run open-source models locally, exposes OpenAI-compatible API on localhost