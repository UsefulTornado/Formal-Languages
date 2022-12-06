from collections import defaultdict
from copy import deepcopy


class Nonterminal:
    def __init__(self, symbol, mark=None):
        self.symbol = symbol
        self.mark = mark

    def __eq__(self, other):
        return (isinstance(other, Nonterminal) and
                self.symbol == other.symbol and
                self.mark == other.mark)

    def __hash__(self):
        return hash(self.symbol)

    def __str__(self):
        if self.mark:
            return f'{self.symbol}_{self.mark.symbol}'
        return self.symbol


class Terminal:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return (isinstance(other, Terminal) and
                self.symbol == other.symbol)

    def __hash__(self):
        return hash(self.symbol)

    def __str__(self):
        return self.symbol


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Rule) and
                self.left == other.left and
                self.right == other.right)
    
    def __str__(self):
        return f'{self.left} -> {" ".join(map(str, self.right))}'


class CFGrammar:
    def __init__(self, start=Nonterminal('S'), rules=None):
        self.start = start
        self.rules = rules or []
        self.nonterminals = self._get_nonterminals()
        self.rules_by_nonterminals = self._get_rules_by_nonterminals()

    def __str__(self):
        return ('Starting: ' + str(self.start) + '\n' +
                'Nonterminals: ' + " ".join(map(str, self.nonterminals)) + '\n\n' +
                'Rules:\n\n' +
                '\n'.join(map(str, self.rules)))

    def _get_nonterminals(self):
        nonterminals = set()
        for rule in self.rules:
            nonterminals.add(rule.left)
            nonterminals.update({sym for sym in rule.right if isinstance(sym, Nonterminal)})
        return nonterminals
    
    def _get_rules_by_nonterminals(self):
        rules_by_nts = defaultdict(list)
        for rule in self.rules:
            rules_by_nts[rule.left].append(rule)
        return rules_by_nts

    def _new_nonterminal(self, sym):
        suffix = 0
        sym = sym.upper()
        while Nonterminal(sym + str(suffix)) in self.nonterminals:
            suffix += 1
        return Nonterminal(sym + str(suffix))

    def first(self, k, symbols):
        def cartesian_product(set1, set2, max_num):
            if not set1:
                return set2
            if not set2:
                return set1
            return {(a + b)[:max_num] for a in set1 for b in set2}

        def first_rec(k, symbols, visited):
            if k == 0:
                return set()

            if not symbols:
                return {tuple()}

            if isinstance(symbols[0], Terminal):
                return cartesian_product(
                    {(symbols[0], )},
                    first_rec(k - 1, symbols[1:], visited),
                    max_num=k
                )

            curr_visited = deepcopy(visited)
            first = set()
            
            for rule in self.rules_by_nonterminals[symbols[0]]:
                if rule.right and rule.right[0] == symbols[0] and symbols[0] in curr_visited:
                    first |= cartesian_product(
                        first_rec(k - 1, rule.right, curr_visited),
                        first_rec(k - 1, symbols[1:], curr_visited),
                        max_num=k
                    )
                else:
                    curr_visited.add(symbols[0])
                    first |= first_rec(k, rule.right + symbols[1:], curr_visited)

            return first

        return first_rec(k, symbols, set())

    def follow(self, k, nonterminal):
        def follow_rec(k, nonterminal):
            if nonterminal == new_start:
                return {(Terminal('$'), )}

            if nonterminal in visited:
                return set()
            visited.add(nonterminal)

            follow = set()

            for rule in self.rules:
                if nonterminal in rule.right:
                    idx = rule.right.index(nonterminal)
                    previous = rule.right[idx+1:]
                    following = follow_rec(k, rule.left)
                    if following:
                        for flw in following:
                            follow |= self.first(k, previous + list(flw))
                    elif previous:
                        follow |= self.first(k, previous)

            return follow
        
        new_start = self._new_nonterminal(self.start.symbol)
        self.rules.append(Rule(new_start, [self.start]))
        visited = set()
        res = follow_rec(k, nonterminal)
        self.rules.pop()
        return res
