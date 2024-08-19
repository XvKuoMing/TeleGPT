from config.openai_config import BASE_SYSTEM_PROMPT, MODEL, client
from typing import Optional, List
import re

comments = re.compile(r"\*.*\*")

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
    if res is None:
        return "К сожалению бот пока не может ответить"
    text = res.choices[0].message.content
    if (text[0] + text[-1]) == "**":
        text = text[1:-1]
    else:
        text = comments.sub("", text)
    return text
