from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()  # load .env vars

API_KEY = os.getenv('OPENAI_TOKEN')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
MODEL = os.getenv('MODEL')

# Read the base system prompt
print("configuring base system prompt")
with open("config/system.txt", 'r', encoding='utf8') as base_file:
    BASE_SYSTEM_PROMPT = base_file.read().replace('\n', ' ')

# Initialize an empty dictionary for system prompts
SYSTEM_PROMPTS = {}

# Iterate over prompt files in the specified directory
# Get the absolute path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # This will get the directory of the current file
# Adjust to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..'))
# accessing the prompts directory
PROMPTS_DIR = os.path.join(PROJECT_ROOT, 'prompts')
print("loading various functions")
for prompt_file in os.listdir(PROMPTS_DIR):
    name = prompt_file.split(".")[0]
    with open(os.path.join(PROMPTS_DIR, prompt_file), encoding="utf-8") as prompt:
        prompt_content = prompt.read().replace("\n", " ")
        SYSTEM_PROMPTS[name] = prompt_content

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=OPENAI_BASE_URL
)
