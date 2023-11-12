from voice_automatisation import (
    detection,
    example_commands,
    interpretation,
    recognition,
)
from voice_automatisation.config import calibrate, config

device_index = None  # device_selection.dialog()

if not ("noise_level" in config and "speech_level" in config):
    calibrate()


for segment in detection.listen():
    transcription = recognition.transcribe(segment)
    command = interpretation.get_associated_command(example_commands, transcription)
    if command is None:
        print(f"Could not decipher that bollocks: {transcription}")
    else:
        command.callback()
        print(f"Called a command: {command.identifier}")
