from config.bot_config import ESCAPE_FROM_MARK


async def escape(self, text: str) -> str:
    for ch in ESCAPE_FROM_MARK:
        text = text.replace(ch, f"\\{ch}")
    return text