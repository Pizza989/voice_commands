import json
import select
import sys
import time
from pathlib import Path

import numpy as np
import pyaudio

from ..core.audio_device import Device
from ..core.audio_processing_utils import mean_spectogram_from_buffer

BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "config.json"
CONFIG_PATH.touch(exist_ok=True)


def set_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file)


def calibrate():
    print(
        "This is the calibration programm. "
        "It will determine the noise and speech levels for your device."
    )
    input("Press Enter to continue...")
    mean_spectogram = []

    device = Device()

    print("Wait while the noise level is being determined.\n")

    with device.open(**stream_data) as stream:
        start = time.time()
        while stream.is_active():
            buffer = stream.read(512)
            mean_spectogram.append(mean_spectogram_from_buffer(buffer))
            if time.time() - start > 1:
                stream.stop_stream()

    config["noise_level"] = max(mean_spectogram)
    mean_spectogram.clear()

    print("The programm will now determin the speech level.")
    print("Press Enter after you said something...")
    with device.open(**stream_data) as stream:
        while stream.is_active():
            buffer = stream.read(512)
            mean_spectogram.append(mean_spectogram_from_buffer(buffer))

            if select.select([sys.stdin], [], [], 0.0)[0]:
                input_data = sys.stdin.readline()
                if input_data:
                    break

    config["speech_level"] = max(mean_spectogram)
    stream.close()
    set_config(config)


with open(CONFIG_PATH, "r") as file:
    try:
        config = json.load(file)
    except json.decoder.JSONDecodeError:
        config = {}

config["samplerate"] = 16000
if not (ratio := config.get("min_speech_volume_ratio", None)):
    config["min_speech_volume_ratio"] = 0.2

set_config(config)

pyaudio_dtype = pyaudio.paInt16
numpy_dtype = np.int16

stream_data = {
    "format": pyaudio_dtype,
    "rate": config["samplerate"],
    "input": True,
    "channels": 1,
}
