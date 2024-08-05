from typing import Iterator, TypedDict
import re
from collections import defaultdict

from . import SearchModel, ConfigModel, SearchResult

class Claim(TypedDict):
    content: str
    subject: str
    position: tuple[int, int]
    

class ClaimModel:
    def __init__(self, claims: str, setting: ConfigModel) -> None:
        self._claims = claims
        self.search = SearchModel("")
        self.setting = setting
        self._unclear_words = self.setting.load_unclear_words()

    def reset_claims(self, claims: str) -> None:
        self._claims = claims

    def check_unclear_words(self) -> Iterator[SearchResult]:
        self.search.reset_search_model(self._claims)
        self.search.set_search_pattern("|".join(self._unclear_words))
        return self.search.search()

    def _parse_claims(self) -> None:
        pattern = r"^(\d+)\s*[.、]\s*([^，]+)，(?:.|\n(?!^\d|$))+"
        self.search.set_search_pattern(pattern, re.MULTILINE)
        self.search.reset_search_model(content=self._claims)
        self.claims = defaultdict(dict)
        for match, start, end in self.search.search():
            claim_num = int(match.group(1))
            self.claims[claim_num]["content"] = match.group(0)
            self.claims[claim_num]["subject"] = match.group(2)
            self.claims[claim_num]["position"] = (start, end)