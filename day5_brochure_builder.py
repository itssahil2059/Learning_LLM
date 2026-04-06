# Day 5 - Company Brochure Builder
# Full business solution — scrape website → AI filters links → AI generates brochure → streaming output
# Ed Donner LLM Engineering Course

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
openai = OpenAI()
MODEL = "gpt-4o-mini"

# ── STEP 1: System prompt — tells AI which links are relevant ──
link_system_prompt = """
You are provided with a list of links found on a webpage.
Decide which links are most relevant for a company brochure —
such as About, Careers, or Company pages.
Respond in JSON like this:
{
    "links": [
        {"type": "about page", "url": "https://full.url/about"},
        {"type": "careers page", "url": "https://full.url/careers"}
    ]
}
"""

# ── STEP 2: Build user prompt with actual links from the site ──
def get_links_user_prompt(url, links):
    user_prompt = f"""
Here are the links found on {url}.
Pick only the relevant ones for a company brochure.
Respond in JSON. Do not include Terms of Service, Privacy, or email links.

Links:
"""
    user_prompt += "\n".join(links)
    return user_prompt


# ── STEP 3: Ask AI to filter links — uses json_object response format ──
def select_relevant_links(url, links):
    print(f"Selecting relevant links for {url}...")
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user",   "content": get_links_user_prompt(url, links)}
        ],
        response_format={"type": "json_object"}   # forces AI to reply in JSON
    )
    result = response.choices[0].message.content
    links = json.loads(result)                     # convert JSON string → Python dict
    print(f"Found {len(links['links'])} relevant links")
    return links


# ── STEP 4: Brochure system prompt ────────────────────────────
brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages
from a company website and creates a short brochure about the company
for prospective customers, investors and recruits.
Respond in markdown. Include company culture, customers, and careers if available.
"""


# ── STEP 5: Stream the brochure back with typewriter effect ───
def stream_brochure(company_name, page_content):
    print(f"\nGenerating brochure for {company_name}...\n")
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user",   "content": f"Company: {company_name}\n\n{page_content[:5000]}"}
        ],
        stream=True                               # stream=True = typewriter effect
    )
    response = ""
    for chunk in stream:
        piece = chunk.choices[0].delta.content or ""
        response += piece
        print(piece, end="", flush=True)          # print each chunk as it arrives
    print("\n")
    return response


# ── DEMO — run with dummy content ─────────────────────────────
if __name__ == "__main__":
    # Simulating what fetch_website_contents() would return
    dummy_links = [
        "https://huggingface.co/about",
        "https://huggingface.co/careers",
        "https://huggingface.co/privacy",      # should be filtered out
        "mailto:contact@huggingface.co",       # should be filtered out
        "https://huggingface.co/blog",
    ]

    dummy_page_content = """
    HuggingFace is the AI community building the future.
    We host thousands of open source models and datasets.
    Our mission is to democratize good machine learning.
    We are hiring engineers, researchers and product managers.
    Our customers include Google, Microsoft and thousands of startups.
    """

    relevant = select_relevant_links("https://huggingface.co", dummy_links)
    print("Relevant links:", json.dumps(relevant, indent=2))

    stream_brochure("HuggingFace", dummy_page_content)


# ── KEY CONCEPTS LEARNED TODAY ────────────────────────────────
"""
1. response_format={"type": "json_object"}
   → Forces the AI to always reply in valid JSON
   → json.loads() converts JSON string back to Python dict

2. stream=True
   → AI sends response in chunks instead of all at once
   → chunk.choices[0].delta.content gives each piece
   → Creates the typewriter animation effect

3. One-shot prompting
   → You show the AI ONE example of the format you want
   → AI follows that format for its actual response

4. Multi-call AI pipeline (first taste of Agentic AI!)
   → Call 1: scrape website links
   → Call 2: AI filters relevant links (JSON)
   → Call 3: AI generates full brochure (streaming)
   → Combining multiple LLM calls = Agentic AI pattern
"""