import numpy as np

from pvrecorder import PvRecorder
from scipy import signal


def calculate_volume(buffer: list[int]):
    # Apply Hamming window
    hamming_window = np.hamming(len(buffer))
    windowed_samples = buffer * hamming_window

    # Calculate the volume
    volume = np.sum(np.abs(windowed_samples))
    return np.log10(volume) * 20


def resample(buffer: list[int], old: int, new: int):
    resampling_factor = new / old
    return signal.resample(buffer, int(len(buffer) * resampling_factor))


def listen(
    device_index=3,
    frame_length=512,
    sample_rate=16000,
    detection_threshold=100,
    pause_threshold=1,
):
    recorder = PvRecorder(frame_length=frame_length, device_index=device_index)
    recorder.start()

    buffer = []
    is_talking = False
    pause_time = 0

    while recorder.is_recording:
        frame = recorder.read()
        volume = calculate_volume(frame)
        if volume >= detection_threshold:
            is_talking = True
            pause_time = 0
        elif is_talking:
            pause_time += (1 / recorder.sample_rate) * frame_length

        if is_talking:
            buffer.append(frame)
            if pause_time >= pause_threshold:
                if recorder.sample_rate != sample_rate:
                    yield resample(
                        buffer,
                        recorder.sample_rate,
                        sample_rate,
                    )
                else:
                    yield buffer
                # reset values
                buffer.clear()
                is_talking = False
                pause_time = 0
