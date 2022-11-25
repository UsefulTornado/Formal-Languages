import argparse

from bisimulation import Bisimulation
from blum_koch import blum_koch_normalize
from cfg import CFGrammar
from cfg_parser import Parser


def main():
    parser = argparse.ArgumentParser(description="Normalization of a CFG.")
    parser.add_argument(
        "-f", "--file_path",
        help="Path to the file with context-free grammar input data.",
    )
    parser.add_argument(
        "-cnf", "--chomsky", action="store_true",
        help="Whether to use Chomsky normalization."
             "If not specified, Greibach normalization is used.",
    )
    parser.add_argument(
        "-bk", "--blum_koch", action="store_true",
        help="Whether to use Blum-Koch algorithm for Greibach normalization."
             "If not specified, elimination of left recursion is used.",
    )
    parser.add_argument(
        "-bs", "--bisimulate", action="store_true",
        help="Whether to simplify grammar with bisimulation.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Whether to print additional information.",
    )
    args = parser.parse_args()

    with open(args.file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    cfg = CFGrammar(rules=Parser().parse_grammar(lines))

    if args.chomsky:
        normalized_cfg = CFGrammar.to_chomsky_normal_form(cfg)
        print(normalized_cfg)
    else:
        if args.blum_koch:
            normalized_cfg, nfas = blum_koch_normalize(cfg)
            print(normalized_cfg)
            if args.verbose:
                print('\nNFAs for sentential forms:\n')
                for nfa in nfas:
                    print(nfa, end='\n\n')
        else:
            normalized_cfg, ordered_nonterminals = CFGrammar.to_greibach_normal_form(cfg)
            print(normalized_cfg)
            if args.verbose:
                print('\nOrder of nonterminals:',
                      ' > '.join(map(str, ordered_nonterminals)))

    if args.bisimulate:
        print('\nBisimilar grammar:\n\n',
              Bisimulation(normalized_cfg).get_bisimilar_grammar(), sep='')


if __name__ == "__main__":
    main()
