from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generator, Optional, Union

feedback_generator = Generator[Union[str, "feedback_generator"], None, None]
command_callback = Callable[[str], feedback_generator]


@dataclass
class Keyword:
    synonyms: tuple[str]
    weight: float


@dataclass
class Command:
    identifier: str
    keywords: tuple[Keyword]
    callback: command_callback
