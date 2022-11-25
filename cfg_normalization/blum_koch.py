from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from queue import Queue

from cfg import CFGrammar, Nonterminal, Rule


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

    def __str__(self):
        return (str(self.nonterminal) + '\n' +
                '\n'.join(map(str, self.transitions)))

    def _build(self):
        reachable = {self.nonterminal}
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
                    update(rule.right[0])
                else:
                    in_state = Nonterminal(rule.left.symbol, mark=self.nonterminal)
                    out_state = self.final_state
                    self.transitions.append(Transition(in_state, rule.right, out_state))
                    self.reversed_transitions.append(Transition(out_state, rule.right, in_state))
    
    def reverse(self):
        self.transitions, self.reversed_transitions = self.reversed_transitions, self.transitions
        self.start_state, self.final_state = self.final_state, self.start_state

    def _to_list(self, x):
        if isinstance(x, list):
            return x
        return [x]

    def get_grammar(self):
        rules = []
        contains_transitions = any(tr.in_state == self.final_state for tr in self.transitions)

        for transition in self.transitions:
            if transition.out_state == self.final_state:
                rules.append(Rule(transition.in_state,
                                  self._to_list(transition.transit)))
            if transition.out_state != self.final_state or contains_transitions:
                rules.append(Rule(transition.in_state,
                              self._to_list(transition.transit) + self._to_list(transition.out_state)))

        return CFGrammar(self.start_state, rules)


def blum_koch_normalize(cfg):
    cfg = CFGrammar.to_chomsky_normal_form(cfg)

    nt_grammars = {}
    nfas = []

    def build_grammar_by_nonterminal(nt):
        nfa = NFA(cfg, nt)
        nfa.reverse()
        nfas.append(nfa)
        cfg_ = nfa.get_grammar()
        nt_grammars[nt] = cfg_

    def get_rules_by_nonterminal(nt):
        grammar = nt_grammars[nt]
        return list(filter(lambda rule: rule.left == grammar.start, grammar.rules))
    
    build_grammar_by_nonterminal(cfg.start)
    new_cfg = nt_grammars[cfg.start]
    new_rules = deepcopy(new_cfg.rules)
    rules_to_remove_indices = []
    
    for idx, rule in enumerate(new_rules):
        for sym_idx, sym in enumerate(rule.right):
            if isinstance(sym, Nonterminal) and not sym.mark:
                if sym not in nt_grammars:
                    build_grammar_by_nonterminal(sym)
                    new_rules.extend(nt_grammars[sym].rules)
                rules_to_remove_indices.append(idx)
                if sym_idx == 0:
                    new_rules.extend([Rule(rule.left, ext_rule.right + rule.right[1:])
                                        for ext_rule in get_rules_by_nonterminal(sym)])
                else:
                    new_rules.append(
                        Rule(rule.left,
                             rule.right[:sym_idx] + [nt_grammars[sym].start] + rule.right[sym_idx+1:]))
                
    for idx in rules_to_remove_indices[::-1]:
        new_rules.pop(idx)
                
    if Rule(cfg.start, []) in cfg.rules:
        new_rules.append(Rule(new_cfg.start, []))

    return CFGrammar(new_cfg.start, new_rules), nfas
