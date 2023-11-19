from ..dataclasses import Command, Interaction


def start_interaction(interaction: Interaction, assistant, feedback: str = ""):
    assistant.on_interaction(interaction)
    print(interaction.text)  # TODO: say this
    if interaction.is_finished:
        return
    if interaction := interaction.callback(feedback):
        if interaction.needs_feedback:
            feedback = assistant.model.transcribe(assistant.vad.listen())
        start_interaction(interaction, assistant, feedback)


def execute_command(command: Command, assistant, transcription: str):
    start_interaction(command.interaction, assistant, transcription)
