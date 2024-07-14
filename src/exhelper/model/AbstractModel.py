from . import SearchModel, ConfigModel

class AbstractModel:
    def __init__(self, abstract: str, setting: ConfigModel) -> None:
        self.search = SearchModel("")

        self.setting = setting
        
        self._abstract = abstract
        self._abstract_word_pattern = self.setting.load_check_pattern("abstract_word")[0]

    def reset_abstract(self, abstract: str) -> None:
        self._abstract = abstract

    def count_abstract_words_number(self) -> int:
        self.search.reset_search_model(self._abstract)
        self.search.set_search_pattern(self._abstract_word_pattern)
        return len(list(self.search.search()))