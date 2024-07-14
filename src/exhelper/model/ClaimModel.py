from typing import Iterator

from . import SearchModel, ConfigModel, SearchResult

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