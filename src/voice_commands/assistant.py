from pyaudio import paInt16

from .config import make_config
from .core.executor import execute_command
from .core.interpretation import CommandInterpreter
from .core.recognition import Model
from .core.voice_activity_detection import VADetector
from .types import Command


class Assistant:
    def __init__(
        self,
        wake_word: str,
        commands: list[Command],
        model_name: str,
        input_device_query: str,
        min_speech_volume_ratio: float = 0.2,
        input_device_dtype: int = paInt16,
        verbose=False,
    ) -> None:
        make_config(input_device_query, min_speech_volume_ratio, input_device_dtype)
        self.commands = commands
        self.verbose = verbose

        self.vad = VADetector()
        self.model = Model(model_name)
        self.interpreter = CommandInterpreter(self.commands, wake_word)
        self.__segment_generator = self.vad.listen()

        self._awake = False

    @property
    def is_awake(self):
        return self._awake

    def next_transcription(self):
        segment = next(self.__segment_generator)
        return self.model.transcribe(segment)

    def run(self):
        for segment in self.__segment_generator:
            self.on_voice_activity_detection(segment)
            transcription = self.model.transcribe(segment)
            self.on_transcription(transcription)
            if self._awake:
                if command := self.interpreter.associate(transcription):
                    self.on_command(command)
                    execute_command(command, transcription, self)
                    self._awake = False
                else:
                    self.on_no_associated_command()
            else:
                if self.interpreter.is_wake_word(transcription):
                    self.on_awake()
                    self._awake = True

    def on_voice_activity_detection(self, segment: bytes):
        if self.verbose:
            print("Detected Voice.")

    def on_transcription(self, transcription: str):
        if self.verbose:
            print(f"Transcribed: {transcription}")

    def on_command(self, command: Command):
        if self.verbose:
            print(f"Executing Command: {command.identifier}")

    def on_no_associated_command(self):
        if self.verbose:
            print(f"Couldn't associate transcription with command.")

    def on_awake(self):
        if self.verbose:
            print("Assistant just woke up.")
