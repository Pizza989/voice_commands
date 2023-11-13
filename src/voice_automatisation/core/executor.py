from ..dataclasses import Command, Interaction


def start_interaction(interaction: Interaction):
    print("starting new interaction...")
    print(interaction.text)  # TODO: say this
    if interaction := interaction.callback():
        start_interaction(interaction)


def execute_command(command: Command):
    print(f"executing command: {command.identifier}")
    start_interaction(command.interaction)
