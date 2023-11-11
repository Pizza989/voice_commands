import numpy as np
import whisper

model = whisper.load_model("tiny")


def transcribe(buffer: np.ndarray):
    return model.transcribe(buffer, language="de")
