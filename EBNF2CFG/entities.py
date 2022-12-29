from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Terminal:
    symbol: str


@dataclass
class Nonterminal:
    symbol: str


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
class ConcatNode:
    value: Union[Terminal, Nonterminal, GroupNode, OptionalNode, IterNode]


@dataclass
class AltNode:
    nodes: List[ConcatNode]


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
    rhs: List[Union[Terminal, Nonterminal]]


@dataclass
class CFGrammar:
    start: Nonterminal
    rules: List[CFGRule]