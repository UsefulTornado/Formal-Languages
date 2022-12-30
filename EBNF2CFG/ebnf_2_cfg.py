from collections import defaultdict
from dataclasses import dataclass
from queue import Queue
from typing import List, Union

from entities import (
    RHS,
    AltNode,
    CFGrammar,
    CFGRule,
    Empty,
    GroupNode,
    IterNode,
    Nonterminal,
    OptionalNode,
    Rule,
    Terminal,
)


@dataclass
class CFGRuleExtended:
    lhs: Nonterminal
    rhs: List[Union[AltNode, GroupNode, OptionalNode, IterNode]]


class Converter:
    def __init__(self, gram, nonterminals):
        self.gram = gram
        self.nonterminals = nonterminals
        self.cfg = []
        self.rule_queue = Queue()
        self.cfg_dict = defaultdict(list)

    def new_nonterminal(self, sym):
        suffix = 0
        sym = sym.upper()
        while Nonterminal(sym + str(suffix)) in self.nonterminals:
            suffix += 1
        nonterm = Nonterminal(sym + str(suffix))
        self.nonterminals.append(nonterm)
        return nonterm

    def ebnf_2_cfg(self):
        def set_cfg():
            transform_rules()
            return CFGrammar(self.gram[0].lhs, self.cfg)

        def transform_rules():
            for rule in self.gram:
                self.rule_queue.put(rule)
            while not self.rule_queue.empty():
                rule = self.rule_queue.get()
                process_one_rule(rule)

        def process_one_rule(rule):
            lhs = rule.lhs
            rhs = rule.rhs
            if isinstance(rule, Rule) or isinstance(rhs, RHS):
                for node in rhs.nodes:
                    self.rule_queue.put(CFGRuleExtended(lhs, node))
            elif isinstance(rhs, AltNode):
                process_alt_node(lhs, rhs)
            elif isinstance(rhs, IterNode):
                process_iter_node(lhs, rhs)
            elif isinstance(rhs, OptionalNode):
                process_optional_node(lhs, rhs)
            elif isinstance(rhs, GroupNode):
                process_group_node(lhs, rhs)

        def process_alt_node(lhs, rhs):
            buf = []
            for node in rhs.nodes:
                if (
                    isinstance(node, (Nonterminal, Terminal, Empty))
                    or isinstance(node, Terminal)
                    or isinstance(node, Empty)
                ):
                    buf.append(node)
                else:
                    new_nont = self.new_nonterminal(lhs.symbol)
                    buf.append(new_nont)
                    self.rule_queue.put(CFGRuleExtended(new_nont, node))
            self.cfg.append(CFGRule(lhs, buf))

        def process_iter_node(lhs, rhs):
            new_nont = self.new_nonterminal(lhs.symbol)
            self.cfg.append(CFGRule(lhs, [new_nont, lhs]))
            self.cfg.append(CFGRule(lhs, [Empty("$")]))
            self.rule_queue.put(CFGRuleExtended(new_nont, rhs.value))

        def process_optional_node(lhs, rhs):
            self.cfg.append(CFGRule(lhs, [Empty("$")]))
            self.rule_queue.put(CFGRuleExtended(lhs, rhs.value))

        def process_group_node(lhs, rhs):
            self.rule_queue.put(CFGRuleExtended(lhs, rhs.value))

        return set_cfg()

    def display_one_alt(self, elem, config):
        if isinstance(elem, Terminal):
            print(elem.symbol, end="")
        elif isinstance(elem, Nonterminal):
            print(
                f"{config['nonterminal_start']}{elem.symbol}{config['nonterminal_end']}", end=""
            )
        elif isinstance(elem, Empty):
            print(config["empty"], end="")
        else:
            for part in elem:
                self.display_one_alt(part, config)

    def display_cfg_in_user_syntax(self, config):
        for rule in self.cfg:
            self.cfg_dict[rule.lhs].append(rule.rhs)
        for lhs, rhs in self.cfg_dict.items():
            print(
                f"{config['nonterminal_start']}{lhs.symbol}{config['nonterminal_end']}", end=""
            )
            print(f"{config['assignment']}", end="")
            for i, elem in enumerate(rhs):
                self.display_one_alt(elem, config)
                if i != len(rhs) - 1:
                    print(f"{config['alternative']}", end="")
            print(config["separator"], end="")
