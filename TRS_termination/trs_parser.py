from enum import Enum
from queue import Queue
from typing import List, Optional
from entities import Variable, Constructor, RewritingRule


class Tag(Enum):
    """Represents tags for lexemes."""
    ERROR = 0
    NUMBER = 1
    VAR = 2
    CONS = 3
    LPAREN = 4
    RPAREN = 5
    COMMA = 6
    EQ = 7
    END = 8

class Lexeme():
    """Represents lexemes for lexical analysis."""
    def __init__(self, tag: Tag, value: Optional[str] = None):
        self.tag = tag
        self.value = value

class Parser:
    """Performs syntax and lexical analysis of input data."""
    def __init__(self):
        self.constructors = []
        self.variables = []

    def parse_constructors(self, string: str) -> None:
        """Performs parsing of string with constructors and saves them."""
        string = string.split(' ', 2)[-1]
        self.constructors = list(filter(str.isalpha, string))

    def parse_variables(self, string: str) -> None:
        """Performs parsing of string with variables and saves them."""
        string = string.split(' ', 2)[-1]
        self.variables = list(filter(str.isalpha, string))

    def _rule_lexer(self, rule_str: str) -> Queue:
        lexemes = Queue()

        for s in rule_str:
            if s == '(':
                lexemes.put(Lexeme(Tag.LPAREN, value=s))
            elif s == ')':
                lexemes.put(Lexeme(Tag.RPAREN, value=s))
            elif s == ',':
                lexemes.put(Lexeme(Tag.COMMA, value=s))
            elif s == '=':
                lexemes.put(Lexeme(Tag.EQ, value=s))
            elif s.isalpha():
                if s in self.variables:
                    tag = Tag.VAR
                elif s in self.constructors:
                    tag = Tag.CONS
                else:
                    raise Exception(f'No such variable or constructor: {s}')
                lexemes.put(Lexeme(tag, value=s))

        lexemes.put(Lexeme(Tag.END))
        return lexemes
    
    def _parse_rule(self, rule_str: str) -> RewritingRule:
        lexemes = self._rule_lexer(rule_str)

        def rule():
            left = term()
            assert lexemes.get().tag == Tag.EQ
            right = term()
            return RewritingRule(left, right)

        def term():
            lexeme = lexemes.get()
            if lexeme.tag == Tag.VAR:
                return Variable(lexeme.value)
            if lexeme.tag == Tag.CONS:
                assert lexemes.get().tag == Tag.LPAREN
                args = expr()
                assert lexemes.get().tag == Tag.RPAREN
                return Constructor(lexeme.value, args)

            raise Exception((
                'Wrong order of lexemes. '
                f'Instead of <VAR> or <CONS> lexeme <{lexeme.tag}> '
                f'with "{lexeme.value}" was received'))

        def expr():
            return expr_tail([term()])

        def expr_tail(terms):
            if lexemes.queue[0].tag == Tag.COMMA:
                lexemes.get()
                terms.append(term())
                return expr_tail(terms)
            return terms

        return rule()

    def parse_rules(self, rules: List[str]) -> List[RewritingRule]:
        """Performs parsing of the rules according to the following grammar:
            <R>  ::= <T> = <T>.
            <T>  ::= <variable> | <constructor> ( <E> ).
            <E>  ::= <T> <E'>.
            <E'> ::= , <T> <E'> | .
        """
        rewriting_rules = [self._parse_rule(rule) for rule in rules]
        return rewriting_rules