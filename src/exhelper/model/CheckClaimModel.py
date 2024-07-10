from . import SearchModel, ConfigModel

class CheckClaimModel:
    def __init__(self, claims: str) -> None:
        self._claims = claims
        self.search = SearchModel("")
        self.setting = ConfigModel()

    def check_unclear_words(self) -> None:
        pass