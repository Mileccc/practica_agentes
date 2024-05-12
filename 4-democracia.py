import anthropic
from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import requests
import markdown
import webbrowser
import tempfile
from tqdm import tqdm
import time

load_dotenv()

# API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Clients
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
llama_client = OpenAI(base_url='http://localhost:11434/v1', api_key='llama3')
openai_client = OpenAI(api_key=openai_api_key)

# Colors (unused in HTML output, kept for possible console outputs or further expansions)
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Function to open a file and return its contents as a string


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to simulate a local Llama3 session


def local_llama3(messages):
    system_message = {"role": "system",
                      "content": "You are a software dev with Python expertise"}

    # Ensure messages is a List and each element is properly formatted
    if not isinstance(messages, list):
        messages = [{"role": "user", "content": messages}]
    else:
        messages = [{"role": "user", "content": content}
                    for content in messages]

    # Simulate the local response
    messages.insert(0, system_message)
    return messages
