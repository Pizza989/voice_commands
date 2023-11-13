from ..config import config
from .audio_api import api
from .audio_processing_utils import mean_spectogram_from_buffer


class VADetector:
    def __init__(self, frame_count=512, pause_threshold=1) -> None:
        self.frame_count = frame_count
        self.pause_threshold = pause_threshold

    def listen(self):
        segment = b""
        started_talking = False
        pause_time = 0
        detection_threshold = config["vad"]["min_speech_volume_ratio"] * (
            config["vad"]["speech_level"] - config["vad"]["noise_level"]
        )
        with api.open(**config["input_device_info"]) as stream:
            while stream.is_active():
                buffer = stream.read(self.frame_count, exception_on_overflow=False)
                volume = mean_spectogram_from_buffer(buffer)

                if volume >= detection_threshold:
                    started_talking = True
                    pause_time = 0
                elif started_talking:
                    pause_time += (
                        1 / config["input_device_info"]["rate"]
                    ) * self.frame_count

                if started_talking:
                    segment += buffer
                    if pause_time >= self.pause_threshold:
                        yield segment
                        # reset values
                        segment = b""
                        started_talking = False
                        pause_time = 0
