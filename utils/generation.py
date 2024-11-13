from config.openai_config import BASE_SYSTEM_PROMPT, MODEL, client
from config.dp_config import dp
from aiogram.fsm.storage.base import StorageKey
from typing import Optional, List


async def generate_answer(prompt: str, 
                          system: Optional[str] = None, 
                          history: Optional[List[dict]] = None,
                          base64_images: Optional[list] = None):
    
    if system is None:
        system = BASE_SYSTEM_PROMPT
    system = {'role': 'system', 'content': system}
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

    messages = [system, *history, user]
    res = await client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    try:
        res = res.choices[0].message.content
    except:
        res = "К сожалению бот пока не может ответить. Попробуйте еще раз через пару минут"
    messages.append(
        {"role":"assistant", "content": res}
    )
    return res, messages

async def generate(text: str, 
                   storage_key: StorageKey,
                   base64_images: list = None):
    data = await dp.storage.get_data(key=storage_key)
    history = []
    if 'history' in data.keys():
        history = data['history']
    
    system = None
    if "system" in data.keys():
        system = data["system"]
    
    ai_answer, history = await generate_answer(
                        prompt=text,
                        system=system,
                        history=history,
                        base64_images=base64_images
                    )
    await dp.storage.update_data(key=storage_key,
                                 data={'history': history})
    return ai_answer
    
