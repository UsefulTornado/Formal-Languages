import argparse

from cfg import CFGrammar
from cfg_parser import Parser


def main():
    parser = argparse.ArgumentParser(description="Normalization of a CFG.")
    parser.add_argument(
        "-f", "--file_path",
        help="Path to the file with context-free grammar input data.",
    )
    parser.add_argument(
        "-k", default=1, type=int,
        help="Number of terminals for computing First_k and Follow_k sets.",
    )
    args = parser.parse_args()

    with open(args.file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    cfg = CFGrammar(rules=Parser().parse_grammar(lines))

    for nonterminal in cfg.nonterminals:
        print(f'FIRST_{args.k} set for nonterminal <{nonterminal}>:')
        for w in cfg.first(args.k, [nonterminal]):
            print(''.join(map(str, w)))
        print()
        print(f'FOLLOW_{args.k} set for nonterminal <{nonterminal}>:')
        for w in cfg.follow(args.k, nonterminal):
            print(''.join(map(str, w)))
        print()


if __name__ == "__main__":
    main()
