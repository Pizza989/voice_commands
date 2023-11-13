from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Keyword:
    synonyms: tuple[str]
    weight: float


@dataclass
class Command:
    identifier: str
    keywords: tuple[Keyword]
    interaction: Interaction


@dataclass
class Interaction:
    text: str
    callback: Callable
