# Week 2 - Mini Project: AI Email Writer

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
openai = OpenAI()

def write_email(topic, tone):
    """Generate professional email"""
    pass  # TODO: implement tomorrow

if __name__ == "__main__":
    pass  # TODO: add UI