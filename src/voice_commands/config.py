import json
import select
import sys
import time
from pathlib import Path

from .core.audio_api import api
from .core.audio_processing_utils import mean_spectogram_from_buffer

CONFIG_ROOT = Path("~/.config/voice_commands").expanduser()
CONFIG_ROOT.mkdir(parents=True, exist_ok=True)

INPUT_DEVICE_CONFIG = CONFIG_ROOT / "input_device.json"
VAD_CONFIG = CONFIG_ROOT / "voice_activity_detection.json"


def set_config(config: dict, path):
    with open(path, "w") as file:
        json.dump(config, file)


def get_config(path):
    with open(path, "r") as file:
        return json.load(file)


def get_input_device_info(index: int, dtype: int):
    info = api.get_device_info_by_index(index)
    return {
        "format": dtype,
        "rate": int(info["defaultSampleRate"]),
        "input": True,
        "channels": info["maxInputChannels"],
        "input_device_index": index,
    }


def get_vad_info(input_device_info: dict):
    print(
        "This is the calibration programm. "
        "It will determine the noise and speech levels for your device."
    )
    input("Press Enter to continue...")
    print("Wait while the noise level is being determined.\n")
    mean_spectogram = []

    with api.open(**input_device_info) as stream:
        start = time.time()
        while stream.is_active():
            buffer = stream.read(512, exception_on_overflow=False)
            mean_spectogram.append(mean_spectogram_from_buffer(buffer))
            if time.time() - start > 1:
                stream.stop_stream()

    noise_level = max(mean_spectogram)
    mean_spectogram.clear()

    print("The programm will now determin the speech level.")
    print("Press Enter after you said something...")
    with api.open(**input_device_info) as stream:
        while stream.is_active():
            buffer = stream.read(512, exception_on_overflow=False)
            mean_spectogram.append(mean_spectogram_from_buffer(buffer))

            if select.select([sys.stdin], [], [], 0.0)[0]:
                input_data = sys.stdin.readline()
                if input_data:
                    break

    speech_level = max(mean_spectogram)

    return {"noise_level": noise_level, "speech_level": speech_level}


def make_config(
    device_query: str, min_speech_volume_ratio: float = 0.2, input_device_dtype: int = 8
):
    input_device = api.get_input_device_from_query(device_query)
    input_device_info = get_input_device_info(input_device["index"], input_device_dtype)
    set_config(input_device_info, INPUT_DEVICE_CONFIG)

    try:
        vad_config = get_config(VAD_CONFIG)
        if not ("speech_level" in vad_config and "noise_level" in vad_config):
            vad_config = get_vad_info(input_device_info)
        if not "min_speech_volume_ratio" in vad_config:
            vad_config["min_speech_volume_ratio"] = min_speech_volume_ratio
        set_config(vad_config, VAD_CONFIG)
    except FileNotFoundError:
        vad_info = get_vad_info(input_device_info)
        vad_info["min_speech_volume_ratio"] = min_speech_volume_ratio
        set_config(vad_info, VAD_CONFIG)
