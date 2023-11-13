from vosk import KaldiRecognizer
from vosk import Model as VModel

from ..config import config


class Model(VModel):
    def __init__(self, model_path=None, model_name=None, lang=None):
        super().__init__(model_path, model_name, lang)
        self.recognizer = KaldiRecognizer(self, config["input_device_info"]["rate"])

    def transcribe(self, segment):
        self.recognizer.AcceptWaveform(segment)
        text = self.recognizer.Result()
        return text
