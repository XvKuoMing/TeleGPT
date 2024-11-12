from aiogram.types import Message, BufferedInputFile
from io import BytesIO



async def as_doc(text: str, filename: str):
    if "." in filename:
        print("filename must not have . in its name, it must not contain extension")
        filename = filename.split(".")[0]
    b = BytesIO()
    b.write((text+"\n").encode("utf-8"))
    b.seek(0)
    input_file = BufferedInputFile(b.read(), filename=f"{filename}.txt")
    b.close()
    return input_file