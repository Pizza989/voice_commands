import numpy as np
import sounddevice as sd

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
    device_query=None,
    frame_length=512,
    sample_rate=16000,
    detection_threshold=-20,
    pause_threshold=1,
):
    device = sd.InputStream(samplerate=sample_rate, device=device_query)
    device.start()
    segment = []
    started_talking = False
    pause_time = 0

    while device.active:
        frames, _ = device.read(frame_length)
        frames = frames.mean(axis=1)
        volume = calculate_volume(frames)

        if volume >= detection_threshold:
            started_talking = True
            pause_time = 0
        elif started_talking:
            pause_time += (1 / sample_rate) * len(frames)

        if started_talking:
            segment.extend(frames)
            if pause_time >= pause_threshold:
                yield np.array(segment, dtype=np.float32)
                # reset values
                segment.clear()
                started_talking = False
                pause_time = 0
