import json
import select
import sys
import time
from pathlib import Path

from ..core.audio_api import api, paInt16
from ..core.audio_processing_utils import mean_spectogram_from_buffer

BASE_PATH = Path(__file__).parent
CONFIG_PATH = BASE_PATH / "config.json"
CONFIG_PATH.touch(exist_ok=True)


def set_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file)


def get_config():
    with open(CONFIG_PATH, "r") as file:
        try:
            return json.load(file)
        except json.decoder.JSONDecodeError:
            return {}


def get_input_device_from_query(query: str):
    """Return the first input device that has query in its name

    Args:
        query (str): A case insesitive substring of the wanted device's name

    Returns:
        _type_: dict[str, Any]
    """
    devices = api.get_input_devices()
    for device in devices:
        if query.lower() in device["name"].lower():
            return device


def calibrate():
    print(
        "This is the calibration programm. "
        "It will determine the noise and speech levels for your device."
    )
    input("Press Enter to continue...")
    mean_spectogram = []

    print("Wait while the noise level is being determined.\n")

    with api.open(**config["input_device_info"]) as stream:
        start = time.time()
        while stream.is_active():
            buffer = stream.read(512)
            mean_spectogram.append(mean_spectogram_from_buffer(buffer))
            if time.time() - start > 1:
                stream.stop_stream()

    config["vad"]["noise_level"] = max(mean_spectogram)
    mean_spectogram.clear()

    print("The programm will now determin the speech level.")
    print("Press Enter after you said something...")
    with api.open(**config["input_device_info"]) as stream:
        while stream.is_active():
            buffer = stream.read(512)
            mean_spectogram.append(mean_spectogram_from_buffer(buffer))

            if select.select([sys.stdin], [], [], 0.0)[0]:
                input_data = sys.stdin.readline()
                if input_data:
                    break

    config["vad"]["speech_level"] = max(mean_spectogram)
    stream.close()
    set_config(config)


def make_default_config(
    device_query: str, min_speech_volume_ration=0.2, input_device_dtype=paInt16
):
    # Configure input device
    input_device_index = get_input_device_from_query(device_query)["index"]
    input_device_info = api.get_device_info_by_index(input_device_index)
    input_device_data = {
        "format": input_device_dtype,
        "rate": int(input_device_info["defaultSampleRate"]),
        "input": True,
        "channels": input_device_info["maxInputChannels"],
        "input_device_index": input_device_index,
    }
    config["input_device_info"] = input_device_data

    # Configure voice activity detection
    if not config.get("vad", None):
        config["vad"] = {}
    if not ("noise_level" in config["vad"] and "speech_level" in config["vad"]):
        calibrate()
    if not config["vad"].get("min_speech_volume_ratio", None):
        config["vad"]["min_speech_volume_ratio"] = min_speech_volume_ration

    set_config(config)


config = get_config()
assert "input_device_query" in config
make_default_config(config["input_device_query"])
