# Day 4 - Tokens, Parameters & Context Windows

## Parameters
- Parameters = the "knowledge" stored in a model's weights
- More parameters → more capable, but slower and more expensive
- GPT-4: ~1.8 trillion | LLaMA 3: 8B to 405B | DeepSeek: 671B (MoE)

## Tokens
- LLMs don't read words — they read tokens
- A token ≈ 3/4 of a word
- "chatbot" might be split into "chat" + "bot"
- Use tiktoken library to see how GPT tokenizes text

## Context Window
- The max number of tokens a model can handle (input + output)
- GPT-4o: 128K tokens | Claude: 200K tokens | Gemini: 1M+ tokens
- Bigger context = more info per request, but higher cost

## The "Memory" Illusion
- LLMs don't actually remember previous conversations
- Each API call is independent
- Chat history is re-sent every time as tokens
- That's why long conversations get expensive

## API Cost Formula
- Cost = (input tokens + output tokens) × price per token
- Always be mindful of how much context you're sending