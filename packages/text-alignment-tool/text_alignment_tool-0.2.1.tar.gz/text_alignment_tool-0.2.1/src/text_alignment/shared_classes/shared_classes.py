from dataclasses import dataclass
from typing import NamedTuple
import numpy as np


LetterList = np.ndarray


@dataclass(init=True, frozen=True)
class TextChunk:
    __slots__ = ("indices", "name")
    indices: list[int]
    name: str
