from typing import Callable

from ..dataclasses import Command, Interaction


def start_interaction(interaction: Interaction, on_interaction: Callable = None):
    if on_interaction:
        on_interaction(interaction)
    print(interaction.text)  # TODO: say this
    if interaction := interaction.callback():
        start_interaction(interaction, on_interaction=on_interaction)


def execute_command(command: Command, on_interaction: Callable = None):
    print(f"executing command: {command.identifier}")
    start_interaction(command.interaction, on_interaction=on_interaction)
