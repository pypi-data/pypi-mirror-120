from .alignment_algorithms import (
    AlignmentAlgorithm,
    TextAlignments,
    AlignmentKey,
    AlignmentException,
    GlobalAlignmentAlgorithm,
    LocalAlignmentAlgorithm,
    RoughAlignmentAlgorithm,
    ChunkAlignmentAlgorithm,
)

from .alignment_tool import (
    TextAlignmentException,
    AlignedIndices,
    AlignmentTextDataObject,
    AlignmentOperation,
    TextAlignmentTool,
    get_text_for_range,
    get_text_chunk_string,
    get_text_chunks_string,
    compare_parallel_text_chunks,
    print_parallel_text_chunks,
)

from .find_wordlist_for_alignment import find_wordlist_for_alignment

from .shared_classes import LetterList, TextChunk

from .text_loaders import (
    TextLoader,
    AltoXMLTextLoader,
    PgpXmlTeiTextLoader,
    StringTextLoader,
    NewlineSeparatedTextLoader,
)

from .text_transformers import (
    TextTransformer,
    TransformerError,
    RemoveCharacter,
    RemoveCharacterTransformer,
    CharacterSubstitution,
    SubstituteCharacterTransformer,
    MultipleCharacterSubstitution,
    SubstituteMultipleCharactersTransformer,
    BracketingPair,
    ConsistentBracketingTransformer,
)
