import argparse

from dfa_parser import Parser
from monoid import EquivalenceClass, TransitionMonoid
from utils import print_monoid_details, print_myhill_nerode_details


def main():
    parser = argparse.ArgumentParser(description="Building a transition monoid.")
    parser.add_argument(
        "-f", "--file_path", help="Path to the file with DFA input data."
    )
    parser.add_argument(
        "-mn",
        "--myhill_nerode",
        action="store_true",
        help="Whether to print Myhill–Nerode equivalence classes.",
    )
    args = parser.parse_args()

    with open(args.file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    parser = Parser()
    dfa = parser.parse_dfa(lines)

    if not dfa:
        print("Incorrect data. DFA is not DFA actually.")
    else:
        monoid = TransitionMonoid()
        monoid.build(dfa)
        print_monoid_details(monoid, dfa)
        if args.myhill_nerode:
            classes = [
                EquivalenceClass(word="", pairs={(s, s) for s in dfa.useful_states})
            ] + monoid.classes
            print_myhill_nerode_details(classes, dfa)


if __name__ == "__main__":
    main()
