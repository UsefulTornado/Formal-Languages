import argparse
import json

from grammar_parser import Lexer, Parser
from ebnf_2_cfg import Converter


def main():
    parser = argparse.ArgumentParser(description="Normalization of a CFG.")
    parser.add_argument(
        "-s", "--syntax", default="syntax.json",
        help="Path to the file with custom syntax.",
    )
    parser.add_argument(
        "-g", "--grammar",  default="grammar.txt",
        help="Path to the file with grammar in custom EBNF syntax.",
    )
    parser.add_argument(
        "-sc", "--syntax_cfg", default="cfg_syntax.json",
        help="Path to the file with grammar in custom CFG syntax.",
    )
    args = parser.parse_args()

    with open(args.syntax, mode="r", encoding="utf-8") as file:
        syntax = json.load(file)
    
    with open(args.grammar, mode="r", encoding="utf-8") as file:
        grammar = file.read()

    with open(args.syntax_cfg, mode="r", encoding="utf-8") as file:
        syntax_cfg = json.load(file)

    tokens = Lexer(syntax).tokenize(grammar)
    rules = Parser().parse(tokens)

    converter = Converter(rules, [])
    converter.ebnf_2_cfg()
    converter.display_cfg_in_user_syntax(syntax_cfg)

if __name__ == "__main__":
    main()
