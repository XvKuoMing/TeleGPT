from config.openai_config import BASE_SYSTEM_PROMPT, MODEL, client
from typing import Optional, List
import re

comments = re.compile(r"\*.*\*")

async def generate_answer(prompt: str, 
                          system: Optional[str] = None, 
                          history: Optional[List[dict]] = None,
                          base64_images: Optional[list] = None):
    if system is None:
        system = {'role': 'system', 'content': BASE_SYSTEM_PROMPT}
    if history is None:
        history = []
    
    user =  {"role": "user", "content": None}
    if base64_images:
        user["content"] = [{"type": "text", "text": prompt}]
        for image in base64_images:
            user["content"].append(
                {"type": "image_url", "image_url": {
                    "detail": "high",
                    "url": f"data:image/jpeg;base64,{image}"
                }}
            )
    else:
        user["content"] = prompt


    res = await client.chat.completions.create(
        model=MODEL,
        messages=[
            system,
            *history,
            user
        ]
    )
    try:
        return res.choices[0].message.content
    except:
        return "К сожалению бот пока не может ответить. Попробуй еще раз через пару минут"
    
