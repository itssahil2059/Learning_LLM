# Week 2 - Project: Resume Analyzer
# AI-powered resume analysis and feedback system

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load API keys
load_dotenv(override=True)
openai = OpenAI()
MODEL = "gpt-4.1-mini"

# System message for resume analysis
system_message = """
You are an expert resume analyzer.
Analyze the resume and provide constructive feedback.
"""

def analyze_resume(resume_text):
    """Analyze resume and return feedback"""
    if not resume_text or resume_text.strip() == "":
        return "Please paste your resume text to analyze."
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Analyze this resume:\n\n{resume_text}"}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    
    return response.choices[0].message.content



if __name__ == "__main__":
    pass