from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()  # load .env vars

client = AsyncOpenAI(
    api_key=os.getenv('OPENAI_TOKEN'),
    base_url=os.getenv('OPENAI_BASE_URL')
)
model = os.getenv('MODEL')
system_role = os.getenv('ROLE')

async def generate_answer(prompt: str, role: str = system_role):
    return await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": role,
                "content": prompt
            }
        ]
    )
