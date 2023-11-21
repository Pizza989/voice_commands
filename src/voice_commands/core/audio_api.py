"""
This Module is a representation of my hatred towards pyaudio
its just context managers
"""

from pyaudio import *


class Api(PyAudio):
    def open(self, *args, **kwargs):
        stream = AudioStream(self, *args, **kwargs)
        self._streams.add(stream)
        return stream

    @staticmethod
    def get_input_devices():
        devices = []

        for i in range(api.get_device_count()):
            device_info = api.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                devices.append({"index": i, "name": device_info["name"]})

        return devices

    @staticmethod
    def get_output_devices():
        devices = []

        for i in range(api.get_device_count()):
            device_info = api.get_device_info_by_index(i)
            if device_info["maxOutputChannels"] > 0:
                devices.append({"index": i, "name": device_info["name"]})

        return devices

    @staticmethod
    def get_input_device_from_query(query: str):
        devices = Api.get_input_devices()

        for device in devices:
            if query.lower() in device["name"].lower():
                return device


class AudioStream(Stream):
    def __enter__(self):
        self.start_stream()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()


api = Api()
