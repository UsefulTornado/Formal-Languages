import argparse

from cfg_parser import Parser
from cfg import CFGrammar
from blum_koch import blum_koch


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-f", "--file_path", help="Path to the file with CFG input data.",
    )
    parser.add_argument(
        "-bk", "--blum_koch", action="store_true", help="Whether to use Blum-Koch algorithm.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Whether to print additional information.",
    )
    args = parser.parse_args()

    with open(args.file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    cfg = CFGrammar(rules=Parser().parse_grammar(lines))

    if args.blum_koch:
        greibach_normalized_cfg, nfas = blum_koch(cfg)
        print(f'Starting: {greibach_normalized_cfg.start}')
        print('Nonterminals:', *greibach_normalized_cfg.nonterminals)
        print('\nRules:\n')
        for rule in greibach_normalized_cfg.rules:
            print(rule)

        if args.verbose:
            print('\nNFAs for sentential forms:')
            for nfa in nfas:
                if nfa.transitions:
                    print()
                    print(nfa.nonterminal)
                    for tr in nfa.transitions:
                        print(tr)
    else:
        greibach_normalized_cfg, ordered_nonterminals = CFGrammar.to_greibach_normal_form(cfg)
        print(f'Starting: {greibach_normalized_cfg.start}')
        print('Ordered nonterminals:', *ordered_nonterminals)
        print('\nRules:\n')
        for rule in greibach_normalized_cfg.rules:
            print(rule)


if __name__ == "__main__":
    main()
