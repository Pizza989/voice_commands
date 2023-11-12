from ..config import config, stream_data
from .audio_device import Device
from .audio_processing_utils import mean_spectogram_from_buffer


def listen(
    frame_count=512,
    pause_threshold=1,
):
    segment = b""
    started_talking = False
    pause_time = 0
    detection_threshold = config["min_speech_volume_ratio"] * (
        config["speech_level"] - config["noise_level"]
    )
    with Device().open(**stream_data) as stream:
        while stream.is_active():
            buffer = stream.read(frame_count)
            volume = mean_spectogram_from_buffer(buffer)

            if volume >= detection_threshold:
                started_talking = True
                pause_time = 0
            elif started_talking:
                pause_time += (1 / config["samplerate"]) * frame_count

            if started_talking:
                segment += buffer
                if pause_time >= pause_threshold:
                    yield segment
                    # reset values
                    segment = b""
                    started_talking = False
                    pause_time = 0
