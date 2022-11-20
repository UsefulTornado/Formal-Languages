from queue import Queue
from copy import deepcopy


class Nonterminal:
    def __init__(self, symbol, mark=None):
        self.symbol = symbol
        self.mark = mark

    def __eq__(self, other):
        return isinstance(other, Nonterminal) and self.symbol == other.symbol

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
        return isinstance(other, Terminal) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __str__(self):
        return self.symbol


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            isinstance(other, Rule)
            and self.left == other.left
            and self.right == other.right
        )
    
    def __str__(self):
        return f'{self.left} -> {" ".join(list(map(str, self.right)))}'


class CFGrammar:
    def __init__(self, start=Nonterminal('S'), rules=None):
        self.start = start
        self.rules = rules or []
        self.nonterminals = self._get_nonterminals()

    def _get_nonterminals(self):
        nonterminals = set()
        for rule in self.rules:
            nonterminals.add(rule.left)
            nonterminals.update({sym for sym in rule.right if isinstance(sym, Nonterminal)})
        return nonterminals

    def new_nonterminal(self, sym, used_nonterminals, mark=None):
        suffix = 0
        sym = sym.upper()
        while Nonterminal(sym + str(suffix)) in self.nonterminals | used_nonterminals:
            suffix += 1
        return Nonterminal(sym + str(suffix), mark)

    @staticmethod
    def remove_long_rules(cfg):
        used_nonterminals = set()
        new_rules = []

        def reduce_rule(left, right):
            if len(right) > 2:
                new_left = cfg.new_nonterminal(left.symbol, used_nonterminals)
                used_nonterminals.add(new_left)
                new_rules.append(Rule(left, [right[0], new_left]))
                reduce_rule(new_left, right[1:])
            else:
                new_rules.append(Rule(left, right))

        for rule in cfg.rules:
            reduce_rule(rule.left, rule.right)

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def get_nullable_nonterminals(cfg):
        concerned_rules = {nt: set() for nt in cfg.nonterminals}
        counter = [0] * len(cfg.rules)
        nullable = set()
        nullable_to_process = Queue()

        for idx, rule in enumerate(cfg.rules):
            for sym in rule.right:
                if isinstance(sym, Nonterminal):
                    concerned_rules[sym].add(idx)
                    counter[idx] += 1
            if not rule.right:
                nullable_to_process.put(rule.left)

        while not nullable_to_process.empty():
            left = nullable_to_process.get()
            nullable.add(left)
            for idx in concerned_rules[left]:
                counter[idx] -= 1
                if counter[idx] == 0:
                    nullable_to_process.put(cfg.rules[idx].left)

        return nullable

    @staticmethod
    def remove_nullable_rules(cfg):
        new_rules = []
        nullable = CFGrammar.get_nullable_nonterminals(cfg)

        def update_with_combinations(left, right):
            candidates = Queue()
            candidates.put(right)
            while not candidates.empty():
                rule = Rule(left, candidates.get())
                if rule not in new_rules and rule.right:
                    new_rules.append(rule)
                    for idx, sym in enumerate(rule.right):
                        if sym in nullable:
                            candidates.put(rule.right[:idx] + rule.right[idx+1:])

        for rule in cfg.rules:
            update_with_combinations(rule.left, rule.right)

        if cfg.start in nullable:
            new_start = cfg.new_nonterminal(cfg.start.symbol, set())
            new_rules.append(Rule(new_start, [cfg.start]))
            new_rules.append(Rule(new_start, []))
            return CFGrammar(new_start, new_rules)

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def update_start(cfg):
        new_rules = []
        need_new_start = False
        for rule in cfg.rules:
            if cfg.start in rule.right:
                need_new_start = True
            new_rules.append(rule)

        if need_new_start:
            start = cfg.new_nonterminal(cfg.start.symbol, set())
            new_rules.append(Rule(start, [cfg.start]))
            return CFGrammar(start, new_rules)

        return cfg

    @staticmethod
    def remove_unit_rules(cfg):
        concerned_rules = {nt: set() for nt in cfg.nonterminals}
        new_rules = []
        unit_rules = Queue()

        for idx, rule in enumerate(cfg.rules):
            if len(rule.right) == 1 and rule.right[0] in cfg.nonterminals:
                unit_rules.put(rule)
            else:
                new_rules.append(Rule(rule.left, rule.right))
            concerned_rules[rule.left].add(idx)

        while not unit_rules.empty():
            unit_rule = unit_rules.get()
            for idx in concerned_rules[unit_rule.right[0]]:
                new_rule = Rule(unit_rule.left, cfg.rules[idx].right)
                if (len(new_rule.right) == 1 and new_rule.right[0] in cfg.nonterminals):
                    if new_rule.left != new_rule.right[0]:
                        unit_rules.put(new_rule)
                else:
                    if new_rule not in new_rules:
                        new_rules.append(new_rule)

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def get_generating_nonterminals(cfg):
        concerned_rules = {nt: set() for nt in cfg.nonterminals}
        counter = [0] * len(cfg.rules)
        generating_to_process = Queue()
        generating = set()

        for idx, rule in enumerate(cfg.rules):
            for sym in rule.right:
                if sym in cfg.nonterminals:
                    concerned_rules[sym].add(idx)
                    counter[idx] += 1
            if counter[idx] == 0:
                generating_to_process.put(rule.left)

        while not generating_to_process.empty():
            left = generating_to_process.get()
            for idx in concerned_rules[left]:
                counter[idx] -= 1
                if counter[idx] == 0:
                    generating.add(cfg.rules[idx].left)
                    generating_to_process.put(cfg.rules[idx].left)

        return {cfg.rules[idx].left for idx, cnt in enumerate(counter) if cnt == 0}

    @staticmethod
    def get_reachable_nonterminals(cfg):
        reachable = {cfg.start}
        visited = {nt: False for nt in cfg.nonterminals}

        def visit(nonterminal):
            visited[nonterminal] = True
            for rule in cfg.rules:
                if rule.left == nonterminal:
                    for sym in rule.right:
                        if sym in cfg.nonterminals:
                            reachable.add(sym)
                            if not visited[sym]:
                                visit(sym)

        visit(cfg.start)
        return reachable

    @staticmethod
    def remove_useless_rules(cfg):
        useful_nonterminals = (CFGrammar.get_generating_nonterminals(cfg) &
                               CFGrammar.get_reachable_nonterminals(cfg))
        new_rules = []

        for rule in cfg.rules:
            if rule.left in useful_nonterminals:
                new_rules.append(Rule(rule.left, rule.right))

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def remove_terminal_rules(cfg):
        new_rules = []
        used_nonterminals = set()
        
        for rule in cfg.rules:
            if len(rule.right) == 2:
                right1, right2 = rule.right[0], rule.right[1]
                if right1 not in cfg.nonterminals:
                    new_right1 = cfg.new_nonterminal(right1.symbol, used_nonterminals)
                    used_nonterminals.add(new_right1)
                    new_rules.append(Rule(new_right1, [right1]))
                    right1 = new_right1
                if right2 not in cfg.nonterminals:
                    new_right2 = cfg.new_nonterminal(right2.symbol, used_nonterminals)
                    used_nonterminals.add(new_right2)
                    new_rules.append(Rule(new_right2, [right2]))
                    right2 = new_right2
                new_rules.append(Rule(rule.left, [right1, right2]))
            else:
                new_rules.append(Rule(rule.left, rule.right))

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def arrange_nonterminals(cfg):
        count = {nt: 0 for nt in cfg.nonterminals}
        
        for rule in cfg.rules:
            if rule.right and isinstance(rule.right[0], Nonterminal):
                count[rule.left] += 1

        return [x[0] for x in sorted(count.items(), key=lambda x: -x[1])]

    @staticmethod
    def _remove_rules(rules, indices):
        for idx in indices:
            rules.pop(idx)

    @staticmethod
    def remove_left_recursion(cfg):
        new_rules = deepcopy(cfg.rules)
        
        arranged = CFGrammar.arrange_nonterminals(cfg)
        new_nonterminals = []

        def remove_direct_left_recursion(nonterminal):
            rules_to_remove_indices = []
            new_nonterminal = cfg.new_nonterminal(nonterminal.symbol, set())
            new_nonterminals.append(new_nonterminal)

            for idx in range(len(new_rules)):
                rule = new_rules[idx]
                if rule.left == nonterminal:
                    if rule.right[0] == nonterminal:
                        rules_to_remove_indices.append(idx)
                        new_rules.append(Rule(new_nonterminal, rule.right[1:]))
                        new_rules.append(Rule(new_nonterminal, rule.right[1:] + [new_nonterminal]))
                    else:
                        new_rules.append(Rule(nonterminal, rule.right + [new_nonterminal]))

            CFGrammar._remove_rules(new_rules, rules_to_remove_indices[::-1])
        
        for i in range(len(arranged)):
            for j in range(i):
                rules_to_remove_indices = []
                for idx in range(len(new_rules)):
                    rule = new_rules[idx]
                    if rule.left == arranged[i] and rule.right[0] == arranged[j]:
                        rules_to_remove_indices.append(idx)
                        new_rules.extend(
                            [Rule(arranged[i], ext_rule.right + rule.right[1:])
                            for ext_rule in new_rules if ext_rule.left == arranged[j]])
                CFGrammar._remove_rules(new_rules, rules_to_remove_indices[::-1])

            if any(arranged[i] == rule.left == rule.right[0] for rule in new_rules):
                remove_direct_left_recursion(arranged[i])

        return CFGrammar(cfg.start, new_rules), new_nonterminals[::-1] + arranged

    @staticmethod
    def to_greibach_normal_form(cfg):
        new_cfg = CFGrammar.remove_nullable_rules(cfg)
        new_cfg = CFGrammar.remove_unit_rules(new_cfg)

        nullable_rule = None
        for idx, rule in enumerate(new_cfg.rules):
            if not rule.right:
                nullable_rule = new_cfg.rules.pop(idx)
                break

        new_cfg, ordered_nonterminals = CFGrammar.remove_left_recursion(new_cfg)
        new_rules = deepcopy(new_cfg.rules)
        
        for i in range(len(ordered_nonterminals) - 1, -1, -1):
            for j in range(i+1, len(ordered_nonterminals)):
                rules_to_remove_indices = []
                for idx in range(len(new_rules)):
                    rule = new_rules[idx]
                    if rule.left == ordered_nonterminals[i] and rule.right[0] == ordered_nonterminals[j]:
                        rules_to_remove_indices.append(idx)
                        new_rules.extend(
                            [Rule(ordered_nonterminals[i], ext_rule.right + rule.right[1:])
                            for ext_rule in new_rules if ext_rule.left == ordered_nonterminals[j]])
                CFGrammar._remove_rules(new_rules, rules_to_remove_indices[::-1])
        
        if nullable_rule:
            new_rules.append(nullable_rule)

        return CFGrammar(new_cfg.start, new_rules), ordered_nonterminals

    @staticmethod
    def to_chomsky_normal_form(cfg):
        new_cfg = CFGrammar.remove_long_rules(cfg)
        new_cfg = CFGrammar.remove_nullable_rules(new_cfg)
        # new_cfg = CFGrammar.update_start(new_cfg)
        new_cfg = CFGrammar.remove_unit_rules(new_cfg)
        new_cfg = CFGrammar.remove_useless_rules(new_cfg)
        new_cfg = CFGrammar.remove_terminal_rules(new_cfg)

        return new_cfg
