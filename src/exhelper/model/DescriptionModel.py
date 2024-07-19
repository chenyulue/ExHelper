from typing import Iterator
import re
from collections import defaultdict
from . import SearchModel, ConfigModel, SearchResult

class DescriptionModel:
    def __init__(self, description: str, fig_numbers: str, setting: ConfigModel) -> None:
        self._description = description
        self._figure_numbers = fig_numbers
        self.search = SearchModel("")
        self.setting = setting

        self._description_fignum = defaultdict(list)
        self._drawing_fignum = defaultdict(list)

        self._sensitive_words = self.setting.load_sensitive_words()
        self._figure_numbers_pattern = self.setting.load_check_pattern("figure_number")[0]
        self._figure_separator_pattern = self.setting.load_check_pattern("figure_separator")[0]

    def reset_description(self, description: str, fig_numbers: str) -> None:
        self._description = description
        self._figure_numbers = fig_numbers

    def check_sensitive_words(self) -> Iterator[SearchResult]:
        self.search.reset_search_model(self._description)
        self.search.set_search_pattern("|".join(self._sensitive_words))
        return self.search.search()

    def check_figure_numbers_consistency(self) -> tuple[dict[str, list[tuple[int, int]]], dict[str, list[tuple[int, int]]]]:
        self.search.reset_search_model(self._description)
        self.search.set_search_pattern(self._figure_numbers_pattern)
        description_fignum = self.search.search()

        # 如果附图中包含诸如“图1-3”这样的图号，则说明书中查找到的诸如“4-5”的图序号保留原样而不拆分
        if re.search(r"图[0-9a-zA-Z'()]+-[0-9a-zA-Z'()]+", self._figure_numbers) is not None:
            self._figure_separator_pattern = self._figure_separator_pattern.replace("-", "")

        for match, start, end in description_fignum:
            if re.search(self._figure_separator_pattern, match.group()) is not None:
                for sub_fig in re.split(self._figure_separator_pattern, match.group(1)):
                    self._description_fignum["图"+sub_fig].append((start, end))
            else:
                self._description_fignum[match.group(0)].append((start, end))

        self.search.reset_search_model(self._figure_numbers)
        drawing_fignum = self.search.search()
        for match, start, end in drawing_fignum:
            self._drawing_fignum[match.group(0)].append((start, end))

        extra_fignum_in_description = set(self._description_fignum) - set(self._drawing_fignum)
        extra_fignum_in_drawing = set(self._drawing_fignum) - set(self._description_fignum)

        return (
            {k:v for k, v in self._description_fignum.items() if k in extra_fignum_in_description},
            {k:v for k, v in self._drawing_fignum.items() if k in extra_fignum_in_drawing}
        )

        