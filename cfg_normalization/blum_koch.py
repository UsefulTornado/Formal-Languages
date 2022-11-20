from cfg import Nonterminal, Rule, CFGrammar
from dataclasses import dataclass
from copy import deepcopy
from queue import Queue
from collections import defaultdict


@dataclass
class Transition:
    in_state: Nonterminal
    transit: list
    out_state: Nonterminal

    def __str__(self):
        return f'<{self.in_state}, {list(map(str, self.transit))}> -> {self.out_state}'
    

class NFA:
    def __init__(self, cfg, nonterminal):
        self.cfg = cfg
        self.nonterminal = nonterminal
        self.start_state = Nonterminal(nonterminal.symbol, mark=nonterminal)
        self.final_state = self.cfg.new_nonterminal('N', set(), mark=self.nonterminal)
        self.transitions = []
        self.reversed_transitions = []
        self._build()

    def _build(self):
        reachable = {self.start_state}
        nonterminals_to_visit = Queue()
        nonterminals_to_visit.put(self.nonterminal)

        rules_by_nts = defaultdict(list)
        for rule in self.cfg.rules:
            if rule.right:
                rules_by_nts[rule.left].append(rule)

        def update(sym):
            if isinstance(sym, Nonterminal) and sym not in reachable:
                nonterminals_to_visit.put(sym)
                reachable.add(sym)

        while not nonterminals_to_visit.empty():
            nonterminal = nonterminals_to_visit.get()
            for rule in rules_by_nts[nonterminal]:
                if isinstance(rule.right[0], Nonterminal):
                    in_state = Nonterminal(rule.left.symbol, mark=self.nonterminal)
                    out_state = Nonterminal(rule.right[0].symbol, mark=self.nonterminal)
                    self.transitions.append(Transition(in_state, rule.right[1:], out_state))
                    self.reversed_transitions.append(Transition(out_state, rule.right[1:], in_state))
                else:
                    in_state = Nonterminal(rule.left.symbol, mark=self.nonterminal)
                    out_state = self.final_state
                    self.transitions.append(Transition(in_state, rule.right, out_state))
                    self.reversed_transitions.append(Transition(out_state, rule.right, in_state))
                
                for sym in rule.right:
                    update(sym)

    
    def reverse(self):
        self.transitions, self.reversed_transitions = self.reversed_transitions, self.transitions
        self.start_state, self.final_state = self.final_state, self.start_state

    def _to_list(self, x):
        if isinstance(x, list):
            return x
        return [x]

    def get_grammar(self):
        rules = []
        for transition in self.transitions:
            if transition.out_state == self.final_state:
                rules.append(Rule(transition.in_state,
                                  self._to_list(transition.transit)))
            rules.append(Rule(transition.in_state,
                              self._to_list(transition.transit) + self._to_list(transition.out_state)))

        return CFGrammar(self.start_state, rules)


def blum_koch(cfg):
    cfg = CFGrammar.to_chomsky_normal_form(cfg)
    nt_grammars = {}
    nfas = []
    for nt in cfg.nonterminals:
        nfa = NFA(cfg, nt)
        nfa.reverse()
        nfas.append(nfa)
        nt_grammars[nt] = nfa.get_grammar()

    new_cfg = nt_grammars[cfg.start]
    new_rules = deepcopy(new_cfg.rules)

    def get_rules_by_nonterminal(nt):
        grammar = nt_grammars[nt]
        return list(filter(lambda rule: rule.left == grammar.start, grammar.rules))

    rules_to_remove_indices = []
    for idx in range(len(new_rules)):
        rule = new_rules[idx]
        for sym_idx, sym in enumerate(rule.right):
            if isinstance(sym, Nonterminal) and not sym.mark:
                rules_to_remove_indices.append(idx)
                new_rules.extend(
                    [Rule(
                        rule.left,
                        rule.right[:sym_idx] + ext_rule.right + rule.right[sym_idx+1:]
                    )
                        for ext_rule in get_rules_by_nonterminal(sym)]
                )

    for idx in rules_to_remove_indices[::-1]:
        new_rules.pop(idx)

    return CFGrammar(new_cfg.start, new_rules), nfas
