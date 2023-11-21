import json
from pathlib import Path

from vosk import KaldiRecognizer
from vosk import Model as VModel

from ..config import INPUT_DEVICE_CONFIG, get_config
from ..model_manager import download_model


class Model(VModel):
    def __init__(self, model_name, lang=None):
        models_root = Path("~/.cache/voice_commands/models/").expanduser()
        model_name_path = models_root / model_name

        if not model_name_path.exists():
            print(f"Model of name <{model_name}> does not exist.")
            url = input("Enter the url for the model you want to download: ")
            download_model(url, model_name)

        model_name_path_children = [d for d in model_name_path.iterdir() if d.is_dir()]
        model_path = model_name_path / model_name_path_children[0]

        super().__init__(model_path.as_posix(), model_name, lang)
        config = get_config(INPUT_DEVICE_CONFIG)
        self.recognizer = KaldiRecognizer(self, config["rate"])

    def transcribe(self, segment):
        self.recognizer.AcceptWaveform(segment)
        text = json.loads(self.recognizer.Result())["text"]
        return text
