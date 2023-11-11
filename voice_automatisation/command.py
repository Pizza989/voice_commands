from dataclasses import dataclass
from typing import Callable


@dataclass
class Keyword:
    word: str
    weight: float


@dataclass
class Command:
    identifier: str
    keywords: list[Keyword]
    callback: Callable
