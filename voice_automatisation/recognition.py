import numpy as np
import whisper

model = whisper.load_model("tiny")
print("model loaded.")


def transcribe(buffer: np.ndarray):
    print("Transcriping audio segment...")
    transcription = model.transcribe(buffer, language="de")
    print(transcription)
    return transcription["text"]
