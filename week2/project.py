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
Analyze the resume and provide constructive feedback on:
1. Overall structure and formatting
2. Key strengths identified
3. Areas for improvement
4. Missing keywords for job applications
5. Top 3 actionable suggestions

Be concise, specific, and professional.
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
        messages=messages,
        stream=True
    )

    # Stream response word by word for better UX
    # yield sends partial results as they arrive
    result = ""
    for chunk in response:
        result += chunk.choices[0].delta.content or ""
        yield result



if __name__ == "__main__":
    resume_input = gr.Textbox(
        label="Paste your resume:",
        lines=12,
        placeholder="Copy and paste your resume text here..."
    )
    
    analysis_output = gr.Textbox(
        label="Analysis:",
        lines=15
    )
    
    view = gr.Interface(
    fn=analyze_resume,
    inputs=resume_input,
    outputs=analysis_output,
    title="📄 Resume Analyzer",
    description="Get AI-powered feedback on your resume",
    examples=[
        ["John Doe\nSoftware Engineer\n\nExperience:\n- Built web apps\n- Python, JavaScript\n\nEducation:\nBS Computer Science"],
        ["Jane Smith\nData Scientist\n\nSkills:\n- Machine Learning, SQL, Python\n\nExperience:\n- 3 years analyzing data\n- Built ML models\n\nEducation:\nMS Data Science, MIT"]  # ← add this
    ],
    flagging_mode="never"
)
    
    view.launch()


# ─────────────────────────────────────────
# TODO: Future Features
# ─────────────────────────────────────────
# TODO: Add PDF upload support
# TODO: Add resume scoring (0-100)
# TODO: Add job description comparison
# TODO: Add keyword extraction for ATS optimization
# TODO: Add export analysis as PDF
# TODO: Add multiple resume format support (DOC, DOCX)
# TODO: Add industry-specific analysis (tech, finance, healthcare)