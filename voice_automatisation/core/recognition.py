from vosk import KaldiRecognizer, Model

model = Model(
    r"./voice_automatisation/models/vosk-model-small-de-0.15/vosk-model-small-de-0.15"
)
recognizer = KaldiRecognizer(model, 16000)
print("model loaded.")


def transcribe(segment):
    print("Transcriping audio segment...")
    recognizer.AcceptWaveform(segment)
    text = recognizer.Result()
    print(text)
    return text
