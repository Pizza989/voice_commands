import subprocess
from dataclasses import dataclass

from .interaction import Interaction


@dataclass
class Keyword:
    synonyms: tuple[str]
    weight: float


@dataclass
class Command:
    identifier: str
    keywords: tuple[Keyword]
    interaction: Interaction


def interaction():
    return Interaction("Das hat nicht funktioniert.", lambda: print("fehler"))


example_commands = [
    Command(
        "play/pause",
        (
            Keyword(("wiedergabe",), 5),
            Keyword(("pause", "pausieren", "weiter", "fortführen"), 1),
        ),
        interaction=Interaction(
            "1", lambda: subprocess.call(["xdotool", "run", "XF86AudioPlay"])
        ),
    )
]
