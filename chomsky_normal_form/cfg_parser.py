import re

from cfg import Nonterminal, Rule, Terminal


class Parser:

    pattern = re.compile(r"(\[[a-zA-Z]+[0-9]*\])|([a-zA-Z]|[0-9])")

    def _parse_rule(self, line):
        splitted = self.pattern.split(line)
        symbols = [sym for sym in splitted if sym and self.pattern.match(sym)]
        
        left = Nonterminal(symbols[0][1:-1])
        right = []
        for sym in symbols[1:]:
            if sym[0] == '[':
                right.append(Nonterminal(sym[1:-1]))
            else:
                right.append(Terminal(sym))

        return Rule(left, right)

    def parse_grammar(self, lines):
        return [self._parse_rule(line) for line in lines]
