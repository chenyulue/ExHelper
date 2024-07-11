from . import SearchModel

class CheckClaimModel:
    def __init__(self, claims: str) -> None:
        self._claims = claims
        self.search = SearchModel("")

    def check_unclear_words(self) -> None:
        pass