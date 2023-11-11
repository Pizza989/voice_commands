import json
from pathlib import Path

import numpy as np
import sounddevice as sd

BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "config.json"
CONFIG_PATH.touch(exist_ok=True)


def calibrate():
    with open(CONFIG_PATH, "r") as file:
        try:
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            config = {}

    if not (samplerate := config.get("samplerate", None)):
        samplerate, config["samplerate"] = 16000, 16000
        print(samplerate, config["samplerate"])

    def write_data(indata, frames, time, status):
        spectrogram = np.abs(np.fft.rfft(indata, n=frames))
        mean = spectrogram.mean()
        mean_spectogram.append(mean)

    input(
        "This is the calibration programm. It will determine the noise and speech levels for your device.\nPress Enter to continue..."
    )

    print("Wait while the noise level is being determined.")

    mean_spectogram = []
    with sd.InputStream(samplerate=samplerate, callback=write_data) as stream:
        sd.sleep(1000)

    config["noise_level"] = max(mean_spectogram)
    mean_spectogram.clear()

    print("The programm will now determin the speech level")
    with sd.InputStream(samplerate=samplerate, callback=write_data) as stream:
        input("Press Enter after you said something...")

    config["speech_level"] = max(mean_spectogram)

    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file)
