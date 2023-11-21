from ..config import INPUT_DEVICE_CONFIG, VAD_CONFIG, get_config
from .audio_api import api
from .audio_processing_utils import mean_spectogram_from_buffer


class VADetector:
    def __init__(self, frame_count=512, pause_threshold=1) -> None:
        self.frame_count = frame_count
        self.pause_threshold = pause_threshold

        self.__input_device_config = get_config(INPUT_DEVICE_CONFIG)
        self.__vad_config = get_config(VAD_CONFIG)

    def listen(self):
        segment = b""
        started_talking = False
        pause_time = 0
        detection_threshold = self.__vad_config["min_speech_volume_ratio"] * (
            self.__vad_config["speech_level"] - self.__vad_config["noise_level"]
        )
        with api.open(**self.__input_device_config) as stream:
            while stream.is_active():
                buffer = stream.read(self.frame_count, exception_on_overflow=False)
                volume = mean_spectogram_from_buffer(buffer)

                if volume >= detection_threshold:
                    started_talking = True
                    pause_time = 0
                elif started_talking:
                    pause_time += (
                        1 / self.__input_device_config["rate"]
                    ) * self.frame_count

                if started_talking:
                    segment += buffer
                    if pause_time >= self.pause_threshold:
                        yield segment
                        # reset values
                        segment = b""
                        started_talking = False
                        pause_time = 0
