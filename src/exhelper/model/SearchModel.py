import re
from typing import Iterator, NamedTuple

class SearchResult(NamedTuple):
    match: re.Match[str]
    start: int
    end: int

class SearchModel:
    def __init__(self, content: str, regex: bool=True) -> None:
        self.content = content
        self.pattern = None
        self.use_regex = regex

    def reset_search_model(self, content: str, regex: bool=True) -> None:
        self.content = content
        self.use_regex = regex
        self.pattern = None

    def set_search_pattern(self, pattern: str, *args, **kwargs) -> None:
        try:
            if not self.use_regex:
                pattern = re.escape(pattern)
            self.pattern = re.compile(pattern, *args, **kwargs)
        except re.error:
            raise ValueError(f"Invalid regex pattern: {pattern}")

    def search(self) -> Iterator[SearchResult]:
        if self.pattern is not None:
            match = self.pattern.search(self.content, 0)
            while match is not None:
                start, end = match.span()
                yield SearchResult(match=match, start=start, end=end)
                match = self.pattern.search(self.content, end)
        