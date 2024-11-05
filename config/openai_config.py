from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()  # load .env vars

API_KEY = os.getenv('OPENAI_TOKEN')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
MODEL = os.getenv('MODEL')

# Read the base system prompt
with open("config/system.txt", 'r', encoding='utf8') as base_file:
    BASE_SYSTEM_PROMPT = base_file.read().replace('\n', ' ')

# Initialize an empty dictionary for system prompts
SYSTEM_PROMPTS = {}

# Iterate over prompt files in the specified directory
PROMPTS_DIR = "../prompts/"
for prompt_file in os.listdir(PROMPTS_DIR):
    name = prompt_file.split(".")[0]
    with open(os.path.join(PROMPTS_DIR, prompt_file), encoding="utf-8") as prompt:
        prompt_content = prompt.read().replace("\n", " ")
        SYSTEM_PROMPTS[name] = prompt_content

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=OPENAI_BASE_URL
)
