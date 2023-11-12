import numpy as np


def mean_spectogram_from_buffer(buffer):
    audio_data = np.frombuffer(buffer, dtype=np.int16)
    spectrogram = np.abs(np.fft.rfft(audio_data))
    return spectrogram.mean()
