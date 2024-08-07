import io
import librosa
import soundfile as sf
import vosk
import ast
from config.bot_config import tgpt

model = vosk.Model("./vosk-model-small-ru-0.22")
recognizer = vosk.KaldiRecognizer(model, 16000)

async def voice_file_id2text(voice_file_id: str) -> str:
    raw_voice_byte = io.BytesIO()
    file = await tgpt.get_file(voice_file_id)
    await tgpt.download_file(file.file_path, destination=raw_voice_byte)
    y, sr = librosa.load(raw_voice_byte, sr=16000)
    raw_voice_byte.close()
    voice = io.BytesIO()
    sf.write(voice, y, sr, format="WAV", subtype="PCM_16")
    voice.seek(0)
    while True:
        data = voice.read(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)
    text = recognizer.FinalResult()
    text = ast.literal_eval(text)["text"]
    return text
