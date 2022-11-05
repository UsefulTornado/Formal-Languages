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
    cfg = CFGrammar(start='S', rules=parser.parse_grammar(lines))
    chomsky_normalized_cfg = CFGrammar.to_chomsky_normal_form(cfg)

    print('Starting:', chomsky_normalized_cfg.start)
    print('Nonterminals:', *chomsky_normalized_cfg.nonterminals)
    for rule in chomsky_normalized_cfg.rules:
        print(rule.left, '->', *rule.right)


if __name__ == "__main__":
    main()
