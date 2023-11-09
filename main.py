from voice_automatisation import (
    device_selection,
    detection,
    recognition,
    interpretation,
)
from voice_automatisation.command import example_commands


device_index = None  # device_selection.dialog()

for segment in detection.listen(device_query=device_index):
    transcription = recognition.transcribe(segment)
    command = interpretation.get_associated_command(example_commands, transcription)
    if command is None:
        print(f"Could not decipher that bollocks: {transcription}")
    else:
        command.callback()
        print(f"Called a command: {command.identifier}")
