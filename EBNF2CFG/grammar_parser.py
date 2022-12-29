from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
from queue import Queue
from entities import (
    Rule,
    Terminal,
    Nonterminal,
    RHS,
    AltNode,
    GroupNode,
    OptionalNode,
    IterNode,
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
    ALT = auto()
    CONCAT = auto()
    GROUPSTART = auto()
    GROUPEND = auto()
    OPTSTART = auto()
    OPTEND = auto()
    ITERSTART = auto()
    ITEREND = auto()
    END = auto()


@dataclass
class Token:
    """Represents tokens for lexical analysis."""

    tag: Tag
    value: Optional[str] = None


class Lexer:
    """Performs lexical analysis of input data."""

    def __init__(self, config):
        self.config = config
        self._mapping = {
            config['assignment']: Tag.ASSIGNMENT,
            config['separator']: Tag.SEPARATOR,
            config['alternative']: Tag.ALT,
            config['concatenation']: Tag.CONCAT,
            config['nonterminal_start']: Tag.NSTART,
            config['nonterminal_end']: Tag.NEND,
            config['group_start']: Tag.GROUPSTART,
            config['group_end']: Tag.GROUPEND,
            config['optional_start']: Tag.OPTSTART,
            config['optional_end']: Tag.OPTEND,
            config['iteration_start']: Tag.ITERSTART,
            config['iteration_end']: Tag.ITEREND,
        }

    def tokenize(self, input_str: str) -> Queue:
        tokens = Queue()

        for sym in input_str:
            if sym in self._mapping:
                tokens.put(Token(tag=self._mapping[sym], value=sym))
            elif sym.isalpha():
                if sym.isupper():
                    tag = Tag.NTERM
                else:
                    tag = Tag.TERM
                tokens.put(Token(tag=tag, value=sym))

        tokens.put(Token(tag=Tag.END))
        return tokens


class Parser:
    """Performs syntax analysis of input data."""

    def __init__(self):
        pass

    def parse(self, tokens: Queue) -> List[Rule]:
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
            return factors

        def rhs_factor():
            token = tokens.get()
            if token.tag == Tag.TERM:
                return Terminal(token.value)
            if token.tag == Tag.NSTART:
                token = tokens.get()
                assert token.tag == Tag.NTERM
                assert tokens.get().tag == Tag.NEND
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

        return rules()
