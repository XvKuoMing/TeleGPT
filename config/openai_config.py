from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()  # load .env vars

API_KEY = os.getenv('OPENAI_TOKEN')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
MODEL = os.getenv('MODEL')
BASE_SYSTEM_PROMPT = open("config/system.txt", 'r', encoding='utf8').read().replace('\n', ' ')

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=OPENAI_BASE_URL
)
