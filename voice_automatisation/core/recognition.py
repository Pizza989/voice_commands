from vosk import KaldiRecognizer, Model

from ..config import config

model = Model(
    r"./voice_automatisation/models/vosk-model-small-de-0.15/vosk-model-small-de-0.15"
)
recognizer = KaldiRecognizer(model, config["samplerate"])
print("model loaded.")


def transcribe(segment):
    print("Transcriping audio segment...")
    recognizer.AcceptWaveform(segment)
    text = recognizer.Result()
    print(text)
    return text
