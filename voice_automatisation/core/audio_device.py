"""
This Module is a representation of my hatred towards pyaudio
its just context managers
"""

import pyaudio


class Device(pyaudio.PyAudio):
    def open(self, *args, **kwargs):
        stream = Stream(self, *args, **kwargs)
        self._streams.add(stream)
        return stream


class Stream(pyaudio.Stream):
    def __enter__(self):
        self.start_stream()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
