import re
from dataclasses import dataclass
from enum import Enum, auto
from queue import Queue
from typing import List, Set, Tuple

from entities import (
    RHS,
    AltNode,
    Empty,
    GroupNode,
    IterNode,
    Nonterminal,
    OptionalNode,
    Rule,
    Terminal,
)


class Tag(Enum):
    """Represents tags for tokens."""

    ERROR = auto()
    TERM = auto()
    NTERM = auto()
    NSTART = auto()
    NEND = auto()
    ASSIGNMENT = auto()
    SEPARATOR = auto()
    EPS = auto()
    ALT = auto()
    CONCAT = auto()
    GROUPSTART = auto()
    GROUPEND = auto()
    OPTSTART = auto()
    OPTEND = auto()
    ITERSTART = auto()
    ITEREND = auto()
    UNMATCHED = auto()
    END = auto()


@dataclass
class Token:
    """Represents tokens for lexical analysis."""

    tag: Tag
    value: str = ""


class Lexer:
    """Performs lexical analysis of input data."""

    def __init__(self, config: dict):
        self.config = config
        self._mapping = {
            config["assignment"]: Tag.ASSIGNMENT,
            config["separator"]: Tag.SEPARATOR,
            config["empty"]: Tag.EPS,
            config["alternative"]: Tag.ALT,
            config["nonterminal_start"]: Tag.NSTART,
            config["nonterminal_end"]: Tag.NEND,
            config["group_start"]: Tag.GROUPSTART,
            config["group_end"]: Tag.GROUPEND,
            config["optional_start"]: Tag.OPTSTART,
            config["optional_end"]: Tag.OPTEND,
            config["iteration_start"]: Tag.ITERSTART,
            config["iteration_end"]: Tag.ITEREND,
        }
        if config["concatenation"]:
            self._mapping[config["concatenation"]] = Tag.CONCAT
        self._re_mapping = {
            config["terminal"]: Tag.TERM,
            config["nonterminal"]: Tag.NTERM,
        }

    def _match_token(self, input_str: str) -> Token:
        for pattern, tag in self._re_mapping.items():
            matched = re.match(pattern, input_str)
            if matched:
                return Token(tag=tag, value=matched.group())

        for pattern, tag in self._mapping.items():
            if input_str.startswith(pattern):
                return Token(tag=tag, value=pattern)

        return Token(tag=Tag.UNMATCHED, value=input_str[0])

    def tokenize(self, input_str: str) -> Queue:
        tokens = Queue()
        idx = 0

        while idx < len(input_str):
            token = self._match_token(input_str[idx:])
            if token.tag == Tag.UNMATCHED and token.value.isspace():
                idx += 1
            else:
                tokens.put(token)
                idx += len(token.value)

        tokens.put(Token(tag=Tag.END))
        return tokens


class Parser:
    """Performs syntax analysis of input data."""

    def parse(self, tokens: Queue) -> Tuple[List[Rule], Set[Nonterminal]]:
        nonterminals = set()

        def rules() -> List[Rule]:
            return rest_rules([rule()])

        def rest_rules(rules) -> List[Rule]:
            if tokens.queue[0].tag == Tag.SEPARATOR:
                tokens.get()
                rules.append(rule())
                return rest_rules(rules)
            return rules

        def rule():
            assert tokens.get().tag == Tag.NSTART
            lhs = tokens.get()
            assert lhs.tag == Tag.NTERM
            nonterminals.add(Nonterminal(lhs.value))
            assert tokens.get().tag == Tag.NEND
            assert tokens.get().tag == Tag.ASSIGNMENT
            rhs_ = rhs()
            return Rule(Nonterminal(lhs.value), rhs_)

        def rhs():
            return RHS(rest_rhs([rhs_term()]))

        def rest_rhs(terms):
            if tokens.queue[0].tag == Tag.ALT:
                tokens.get()
                terms.append(rhs_term())
                return rest_rhs(terms)
            return terms

        def rhs_term():
            return AltNode(rest_rhs_term([rhs_factor()]))

        def rest_rhs_term(factors):
            if tokens.queue[0].tag == Tag.CONCAT:
                tokens.get()
                factors.append(rhs_factor())
                return rest_rhs_term(factors)
            if tokens.queue[0].tag in [
                Tag.EPS,
                Tag.TERM,
                Tag.NSTART,
                Tag.GROUPSTART,
                Tag.OPTSTART,
                Tag.ITERSTART,
            ]:
                factors.append(rhs_factor())
                return rest_rhs_term(factors)
            return factors

        def rhs_factor():
            token = tokens.get()
            if token.tag == Tag.EPS:
                return Empty(token.value)
            if token.tag == Tag.TERM:
                return Terminal(token.value)
            if token.tag == Tag.NSTART:
                token = tokens.get()
                assert token.tag == Tag.NTERM
                assert tokens.get().tag == Tag.NEND
                nonterminals.add(Nonterminal(token.value))
                return Nonterminal(token.value)
            if token.tag == Tag.GROUPSTART:
                rhs_ = rhs()
                assert tokens.get().tag == Tag.GROUPEND
                return GroupNode(rhs_)
            if token.tag == Tag.OPTSTART:
                rhs_ = rhs()
                assert tokens.get().tag == Tag.OPTEND
                return OptionalNode(rhs_)
            if token.tag == Tag.ITERSTART:
                rhs_ = rhs()
                assert tokens.get().tag == Tag.ITEREND
                return IterNode(rhs_)
            raise Exception(f"Wrong Factor <{token.tag}> with value <{token.value}>")

        rules_ = rules()
        return rules_, nonterminals
