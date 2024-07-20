from config.openai_config import BASE_SYSTEM_PROMPT, MODEL, client
from typing import Optional, List

async def generate_answer(prompt: str, system: dict = BASE_SYSTEM_PROMPT, history: Optional[List[dict]] = None):
    system = {'role': 'system', 'content': system}
    if history is None:
        history = []
    res = await client.chat.completions.create(
        model=MODEL,
        messages=[
            system,
            *history,
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return res.choices[0].message.content
