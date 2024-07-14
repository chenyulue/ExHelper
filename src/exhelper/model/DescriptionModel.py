from typing import Iterator
from . import SearchModel, ConfigModel, SearchResult

class DescriptionModel:
    def __init__(self, description: str, fig_numbers: str, setting: ConfigModel) -> None:
        self._description = description
        self._figure_numbers = fig_numbers
        self.search = SearchModel("")
        self.setting = setting

        self._sensitive_words = self.setting.load_sensitive_words()

    def reset_description(self, description: str, fig_numbers: str) -> None:
        self._description = description
        self._figure_numbers = fig_numbers

    def check_sensitive_words(self) -> Iterator[SearchResult]:
        self.search.reset_search_model(self._description)
        self.search.set_search_pattern("|".join(self._sensitive_words))
        return self.search.search()