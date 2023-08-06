from dataclasses import dataclass
import numpy as np


LetterList = np.ndarray


@dataclass(init=True, frozen=True)
class TextChunk:
    __slots__ = ("indices", "name")
    indices: list[int]
    name: str
