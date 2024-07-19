import re
from typing import Iterator, NamedTuple

class SearchResult(NamedTuple):
    match: re.Match[str]
    start: int
    end: int

class SearchModel:
    def __init__(self, content: str, regex: bool=True, pattern: str|None=None) -> None:
        self.content = content
        self.use_regex = regex
        self.pattern = None
        if pattern is not None:
            self.reset_search_model(pattern)

    def reset_search_model(self, content: str|None=None, regex: bool|None=None, pattern: str|None=None) -> None:
        if content is not None:
            self.content = content
        if regex is not None:
            self.use_regex = regex
        if regex is not None:
            self.reset_search_model(pattern)

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
        