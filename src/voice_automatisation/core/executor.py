from ..types import Command, command_callback


def handle_feedback(generator, assistant):
    for feedback in generator:
        t = type(feedback)
        if t is str:
            print(feedback)
        elif callable(t):
            handle_feedback(feedback(assistant.next_transcription()), assistant)
            break
        else:
            raise RuntimeError(
                f"got unexpected feedback type. allowed types are str | {command_callback}"
            )


def execute_command(command: Command, transcription: str, assistant):
    handle_feedback(command.callback(transcription), assistant)
