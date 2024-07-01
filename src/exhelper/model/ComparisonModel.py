from typing import Iterator, TypeAlias, Literal, NamedTuple

import cydifflib as difflib

Tag: TypeAlias = Literal["replace", "delete", "insert", "equal"]

class ComparisonResult(NamedTuple):
    tag: Tag
    a: str
    b: str

class ComparisonModel(difflib.SequenceMatcher): # type: ignore
    def __init__(self, text_modified: str, text_original: str) -> None:
        super().__init__(a=text_original, b=text_modified, autojunk=False)
        
        self.text_original = text_original
        self.text_modified = text_modified

    def reset_texts(self, text_modified: str, text_original: str) -> None:
        self.set_seqs(a=text_original, b=text_modified)
        self.text_original = text_original
        self.text_modified = text_modified

    def get_comparison_sequence(self) -> Iterator[ComparisonResult]:
        for tag, i1, i2, j1, j2 in self.get_opcodes():
            yield ComparisonResult(tag, self.text_original[i1:i2], self.text_modified[j1:j2])
        

    def get_similarity_ratio(self) -> float:
        return self.ratio()

    