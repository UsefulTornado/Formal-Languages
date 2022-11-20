import argparse

from cfg_parser import Parser
from cfg import CFGrammar


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-f", "--file_path", help="Path to the file with CFG input data."
    )
    args = parser.parse_args()

    with open(args.file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    parser = Parser()
    cfg = CFGrammar(rules=parser.parse_grammar(lines))
    # chomsky_normalized_cfg = CFGrammar.to_chomsky_normal_form(cfg)
    greibach_normalized_cfg, ordered_nonterminals = CFGrammar.to_greibach_normal_form(cfg)

    # print('Starting:', chomsky_normalized_cfg.start.symbol)
    # print('Nonterminals:', *[nt.symbol for nt in chomsky_normalized_cfg.nonterminals])
    # for rule in chomsky_normalized_cfg.rules:
    #     print(rule.left.symbol, '->', *[el.symbol for el in rule.right])

    print('Order:', *[nt.symbol for nt in ordered_nonterminals])
    print('Starting:', greibach_normalized_cfg.start.symbol)
    # print('Nonterminals:', *[nt.symbol for nt in greibach_normalized_cfg.nonterminals])
    for rule in greibach_normalized_cfg.rules:
        print(rule.left.symbol, '->', *[el.symbol for el in rule.right])


if __name__ == "__main__":
    main()
