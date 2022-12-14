from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Empty:
    symbol: str


@dataclass
class Terminal:
    symbol: str


@dataclass
class Nonterminal:
    symbol: str

    def __eq__(self, other):
        return isinstance(other, Nonterminal) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


@dataclass
class GroupNode:
    value: Optional[None]


@dataclass
class OptionalNode:
    value: Optional[None]


@dataclass
class IterNode:
    value: Optional[None]


@dataclass
class AltNode:
    nodes: List[Union[Empty, Terminal, Nonterminal, GroupNode, OptionalNode, IterNode]]


@dataclass
class RHS:
    nodes: List[AltNode]


@dataclass
class Rule:
    lhs: Nonterminal
    rhs: RHS


@dataclass
class CFGRule:
    lhs: Nonterminal
    rhs: List[Union[Empty, Terminal, Nonterminal]]


@dataclass
class CFGrammar:
    start: Nonterminal
    rules: List[CFGRule]
