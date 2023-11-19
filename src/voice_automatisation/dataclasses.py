from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


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
    callback: Callable[[str], Optional[Interaction]]
    needs_feedback: bool
    is_finished: bool
