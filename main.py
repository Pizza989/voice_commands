from voice_automatisation import (
    device_selection,
    detection,
    recognition,
    interpretation,
)
from voice_automatisation.command import Command, Keyword


def test_callback():
    print("works.")


device_index = None  # device_selection.dialog()
command_list = [Command("test", [Keyword("hallo", 1)], callback=test_callback)]

for segment in detection.listen(device_query=device_index):
    command = interpretation.get_associated_command(
        command_list,
        recognition.transcribe(segment),
        0,
    )
    if command is None:
        print("Could not decipher that bollocks.")
    else:
        command.callback()
