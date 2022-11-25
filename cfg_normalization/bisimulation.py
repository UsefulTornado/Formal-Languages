from collections import defaultdict

from cfg import CFGrammar, Rule, Terminal


class Bisimulation:
    def __init__(self, cfg):
        self.cfg = cfg
        self.nonterminal_classes = {nt: 0 for nt in cfg.nonterminals}
        self.rules_by_nts = self._get_rules_by_nts()

    def _get_rules_by_nts(self):
        rules_by_nts = defaultdict(list)
        for rule in self.cfg.rules:
            rules_by_nts[rule.left].append(rule)
        
        return rules_by_nts

    def _get_terminal_forms(self):
        forms_to_nonterminals = defaultdict(list)
        
        for nonterminal in self.cfg.nonterminals:
            terminal_forms = set()
            for rule in self.rules_by_nts[nonterminal]:
                terminal_form = ''
                for sym in rule.right:
                    if isinstance(sym, Terminal):
                        terminal_form += sym.symbol
                    else:
                        terminal_form += str(self.nonterminal_classes[sym])
                terminal_forms.add(terminal_form)
            forms_to_nonterminals[tuple(terminal_forms)].append(nonterminal)
        
        return forms_to_nonterminals

    def _update_classes(self, forms_to_nonterminals):
        class_num = 0
        updated = False
        for nonterminals in forms_to_nonterminals.values():
            for nonterminal in nonterminals:
                if self.nonterminal_classes[nonterminal] != class_num:
                    updated = True
                self.nonterminal_classes[nonterminal] = class_num
            class_num += 1
        
        return updated

    def get_bisimilar_grammar(self):
        while self._update_classes(self._get_terminal_forms()):
            pass
        
        class_reprs = {}
        for ntclass, numclass in self.nonterminal_classes.items():
            if numclass not in class_reprs or ntclass == self.cfg.start:
                class_reprs[numclass] = ntclass

        new_rules = []
        for rule in self.cfg.rules:
            new_left = class_reprs[self.nonterminal_classes[rule.left]]
            new_right = []
            for sym in rule.right:
                if isinstance(sym, Terminal):
                    new_right.append(sym)
                else:
                    new_right.append(class_reprs[self.nonterminal_classes[sym]])
            new_rule = Rule(new_left, new_right)
            if new_rule not in new_rules:
                new_rules.append(new_rule)
        
        return CFGrammar(self.cfg.start, list(new_rules))
