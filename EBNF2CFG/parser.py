from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
from entities import Rule


class Tag(Enum):
    """Represents tags for tokens."""

    ERROR = auto()
    TERM = auto()
    NTERM = auto()
    ASSIGNMENT = auto()
    SEP = auto()
    GROUPSTART = auto()
    GROUPEND = auto()
    OPTSTART = auto()
    OPTEND = auto()
    ITERSTART = auto()
    ITEREND = auto()


@dataclass
class Token:
    """Represents tokens for lexical analysis."""

    tag: Tag
    value: Optional[str] = None


class Lexer:
    """Performs lexical analysis of input data."""

    def __init__(self, config):
        self.config = config

    def tokenize(self) -> List[Token]:
        raise NotImplementedError


class Parser:
    """Performs syntax analysis of input data."""

    def __init__(self):
        pass

    def parse(self) -> List[Rule]:
        raise NotImplementedError
