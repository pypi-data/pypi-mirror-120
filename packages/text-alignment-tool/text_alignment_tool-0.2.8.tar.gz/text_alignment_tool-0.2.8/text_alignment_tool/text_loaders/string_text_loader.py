from text_alignment_tool.shared_classes import TextChunk, LetterList
from text_alignment_tool.text_loaders.text_loader import TextLoader
import numpy as np


class StringTextLoader(TextLoader):
    def __init__(self, input_text: str):
        super().__init__()
        self._output = np.array([ord(x) for x in input_text])
        self._text_chunk_indices = [
            TextChunk(list(range(0, self.output.size)), "full text")
        ]
        self._input_output_map = [(x, x) for x in range(0, self.output.size)]

    def _load(self) -> LetterList:
        return super()._load()
