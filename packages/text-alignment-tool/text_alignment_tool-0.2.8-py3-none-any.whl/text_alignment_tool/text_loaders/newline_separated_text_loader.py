from text_alignment_tool.shared_classes import TextChunk, LetterList
from text_alignment_tool.text_loaders.text_loader import TextLoader
import numpy as np


class NewlineSeparatedTextLoader(TextLoader):
    def __init__(self, input_text: str):
        super().__init__()
        self._text_chunk_indices = [
            TextChunk([ord(y) for y in x], f"""line {str(idx)}""")
            for idx, x in enumerate(input_text.split("\n"))
        ]
        self._output = np.array([y for x in self.text_chunk_indices for y in x.indices])
        self._input_output_map = [(x, x) for x in range(0, self.output.size)]

    def _load(self) -> LetterList:
        return super()._load()
