import re

from cfg import Rule


class Parser:

    pattern = re.compile(r"\[([a-zA-Z]+[0-9]*)\]|([a-zA-Z]|[0-9])")

    def _parse_rule(self, line):
        splitted = self.pattern.split(line)
        rule = [sym for sym in splitted if sym and self.pattern.match(sym)]
        return rule[0], rule[1:]

    def parse_grammar(self, lines):
        return [Rule(*self._parse_rule(line)) for line in lines]
