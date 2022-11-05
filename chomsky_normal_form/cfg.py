from queue import Queue


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.left == other.left
            and self.right == other.right
        )


class CFGrammar:
    def __init__(self, start="S", rules=None):
        self.start = start
        self.rules = rules or []
        self.nonterminals = {rule.left for rule in self.rules}
        self.used_symbols = {}

    def new_nonterminal(self, sym, used_symbols):
        suffix = 0
        new_sym = sym + str(suffix)
        while new_sym in self.nonterminals | used_symbols:
            suffix += 1
        return sym + str(suffix)

    @staticmethod
    def remove_long_rules(cfg):
        used_symbols = set()
        new_rules = []

        def reduce_rule(left, right):
            if len(right) > 2:
                new_left = cfg.new_nonterminal(left, used_symbols)
                used_symbols.add(new_left)
                new_rules.append(Rule(left, [right[0], new_left]))
                reduce_rule(new_left, right[1:])
            else:
                new_rules.append(Rule(left, right))

        for rule in cfg.rules:
            reduce_rule(rule.left, rule.right)

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def get_nullable_nonterminals(cfg):
        concerned_rules = {nonterminal: set() for nonterminal in cfg.nonterminals}
        counter = [0] * len(cfg.rules)
        nullable = Queue()

        for idx, rule in enumerate(cfg.rules):
            for sym in rule.right:
                contains_nonterminals = False
                if sym in cfg.nonterminals:
                    concerned_rules[sym].add(idx)
                    counter[idx] += 1
                    contains_nonterminals = True
                if not contains_nonterminals:
                    counter[idx] = -1
            if counter[idx] == 0:
                nullable.put(rule.left)

        while not nullable.empty():
            left = nullable.get()
            for idx in concerned_rules[left]:
                counter[idx] -= 1
                if counter[idx] == 0:
                    nullable.put(cfg.rules[idx].left)

        return {cfg.rules[idx].left for idx, cnt in enumerate(counter) if cnt == 0}

    @staticmethod
    def remove_nullable_rules(cfg):
        new_rules = []
        nullable = CFGrammar.get_nullable_nonterminals(cfg)

        def update_with_combinations(left, right):
            candidates = Queue()
            candidates.put(right)
            while not candidates.empty():
                rule = Rule(left, candidates.get())
                if rule not in new_rules:
                    if rule.right:
                        new_rules.append(rule)
                        for idx, sym in enumerate(rule.right):
                            if sym in nullable:
                                candidates.put(rule.right[:idx] + rule.right[idx + 1 :])
                    elif rule.left == cfg.start:
                        new_rules.append(rule)

        for rule in cfg.rules:
            update_with_combinations(rule.left, rule.right)

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
            start = cfg.new_nonterminal(cfg.start, set())
            new_rules.append(Rule(start, [cfg.start]))
            return CFGrammar(start, new_rules)

        return cfg

    @staticmethod
    def remove_unit_rules(cfg):
        concerned_rules = {nonterminal: set() for nonterminal in cfg.nonterminals}
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
            # print(unit_rule.left, unit_rule.right)
            for idx in concerned_rules[unit_rule.right[0]]:
                new_rule = Rule(unit_rule.left, cfg.rules[idx].right)
                if (
                    len(new_rule.right) == 1
                    and new_rule.right[0] in cfg.nonterminals
                    and new_rule.left != new_rule.right[0]
                ):
                    unit_rules.put(new_rule)
                else:
                    new_rules.append(new_rule)

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def get_generating_nonterminals(cfg):
        concerned_rules = {nonterminal: set() for nonterminal in cfg.nonterminals}
        counter = [0] * len(cfg.rules)
        generating = Queue()

        for idx, rule in enumerate(cfg.rules):
            for sym in rule.right:
                if sym in cfg.nonterminals:
                    concerned_rules[sym].add(idx)
                    counter[idx] += 1
            if counter[idx] == 0:
                generating.put(rule.left)

        while not generating.empty():
            left = generating.get()
            for idx in concerned_rules[left]:
                counter[idx] -= 1
                if counter[idx] == 0:
                    generating.put(cfg.rules[idx].left)

        return {cfg.rules[idx].left for idx, cnt in enumerate(counter) if cnt == 0}

    @staticmethod
    def get_reachable_nonterminals(cfg):
        reachable = {cfg.start}
        visited = {nonterminal: False for nonterminal in cfg.nonterminals}

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
        useful_nonterminals = CFGrammar.get_generating_nonterminals(
            cfg
        ) & CFGrammar.get_reachable_nonterminals(cfg)
        new_rules = []

        for rule in cfg.rules:
            if rule.left in useful_nonterminals:
                new_rules.append(Rule(rule.left, rule.right))

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def remove_terminal_rules(cfg):
        new_rules = []
        used_symbols = set()
        for rule in cfg.rules:
            if len(rule.right) == 2:
                right1, right2 = rule.right[0], rule.right[1]
                if right1 not in cfg.nonterminals:
                    new_right1 = cfg.new_nonterminal(right1, used_symbols)
                    new_rules.append(Rule(new_right1, [right1]))
                    right1 = new_right1
                if right2 not in cfg.nonterminals:
                    new_right2 = cfg.new_nonterminal(right2, used_symbols)
                    new_rules.append(Rule(new_right2, [right2]))
                    right2 = new_right2
                new_rules.append(Rule(rule.left, [right1, right2]))
            else:
                new_rules.append(Rule(rule.left, rule.right))

        return CFGrammar(cfg.start, new_rules)

    @staticmethod
    def to_chomsky_normal_form(cfg):
        new_cfg = CFGrammar.remove_long_rules(cfg)
        new_cfg = CFGrammar.remove_nullable_rules(new_cfg)
        # new_cfg = CFGrammar.update_start(new_cfg)
        new_cfg = CFGrammar.remove_unit_rules(new_cfg)
        new_cfg = CFGrammar.remove_useless_rules(new_cfg)
        new_cfg = CFGrammar.remove_terminal_rules(new_cfg)

        return new_cfg
