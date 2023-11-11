from pathlib import Path

from voice_automatisation import (
    detection,
    device_selection,
    example_commands,
    interpretation,
    recognition,
)
from voice_automatisation.config import calibrate, get_config

device_index = None  # device_selection.dialog()

config = get_config()
if not ("noise_level" in config and "speech_level" in config):
    calibrate()


for segment in detection.listen(device_query=device_index):
    transcription = recognition.transcribe(segment)
    command = interpretation.get_associated_command(example_commands, transcription)
    if command is None:
        print(f"Could not decipher that bollocks: {transcription}")
    else:
        command.callback()
        print(f"Called a command: {command.identifier}")
