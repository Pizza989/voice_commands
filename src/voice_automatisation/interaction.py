from dataclasses import dataclass
from typing import Callable


@dataclass
class Interaction:
    text: str
    callback: Callable
