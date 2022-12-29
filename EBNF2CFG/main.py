import argparse
import json

from grammar_parser import Lexer, Parser


def main():
    parser = argparse.ArgumentParser(description="Normalization of a CFG.")
    parser.add_argument(
        "-s", "--syntax", default="syntax.json",
        help="Path to the file with custom syntax.",
    )
    parser.add_argument(
        "-g", "--grammar",
        help="Path to the file with grammar in custom EBNF syntax.",
    )
    args = parser.parse_args()

    with open(args.syntax, mode="r", encoding="utf-8") as file:
        syntax = json.load(file)
    
    with open(args.grammar, mode="r", encoding="utf-8") as file:
        grammar = file.read()

    tokens = Lexer(syntax).tokenize(grammar)
    rules = Parser().parse(tokens)

if __name__ == "__main__":
    main()
