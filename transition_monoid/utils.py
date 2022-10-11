from tabulate import tabulate


def pretty_print(*text, tabs=0, sep=" "):
    """Prints text with the specified number of tabs and given separator."""
    print("\t" * tabs, end="")
    print(*text, sep=sep)


def print_monoid_details(monoid, dfa):
    """Prints basic information about DFA acceptance of monoid classes combinations."""
    classes = monoid.classes

    print("Rewriting rules:")
    for left, right in monoid.rewriting_rules.items():
        pretty_print(f"{left} -> {right}", tabs=1)

    print("\nEquivalence classes:")
    for cls in classes:
        pretty_print(f"{cls.word} := {cls.pairs}", tabs=1)

    print("\nWords that are accepted by the DFA:")
    pretty_print(
        *[cls.word for cls in classes if dfa.accepts(cls.word)], tabs=1, sep=", "
    )

    print("\nInformation for each class:")
    for cls in classes:
        pretty_print(f'Class w = "{cls.word}":', tabs=1)
        pretty_print('Equivalence classes "v" such that dfa accepts "vw":', tabs=2)
        pretty_print(
            *[
                add_cls.word
                for add_cls in classes
                if dfa.accepts(add_cls.word + cls.word)
            ],
            tabs=3,
            sep=", ",
        )
        pretty_print('Equivalence classes "u" such that dfa accepts "wu":', tabs=2)
        pretty_print(
            *[
                add_cls.word
                for add_cls in classes
                if dfa.accepts(cls.word + add_cls.word)
            ],
            tabs=3,
            sep=", ",
        )
        pretty_print(
            'Equivalence classes "v" and "u" such that dfa accepts "vwu":', tabs=2
        )
        pretty_print(
            *[
                (add1_cls.word, add2_cls.word)
                for add1_cls in classes
                for add2_cls in classes
                if dfa.accepts(add1_cls.word + cls.word + add2_cls.word)
            ],
            tabs=3,
            sep=", ",
        )

        sync_state = dfa.sync_from_word(cls.word)
        pretty_print(
            f"Synchronizes to state: {sync_state}"
            if sync_state
            else "Word is not synchronizing",
            tabs=2,
        )
        print()


def print_myhill_nerode_details(classes, dfa):
    """Prints information about Myhill-Nerode equivalence classes if DFA is minimal."""

    def is_equal(cls1, cls2):
        words1 = {
            add_cls.word for add_cls in classes if dfa.accepts(cls1.word + add_cls.word)
        }
        words2 = {
            add_cls.word for add_cls in classes if dfa.accepts(cls2.word + add_cls.word)
        }
        return words1 == words2

    equivs = [classes[0]]

    for cls in classes[1:]:
        if (
            not any(is_equal(cls, eq) for eq in equivs)
            and dfa.reach_from_state(dfa.initial_state, cls.word) is not None
        ):
            equivs.append(cls)

    if len(equivs) == len(dfa.useful_states):
        table = {"suffixes": []}

        for cls in classes:
            table["suffixes"].append(cls.word)
            table[cls.word] = []

        for suffix in table["suffixes"]:
            for cls in equivs:
                table[cls.word].append("+" if dfa.accepts(cls.word + suffix) else "-")

        print("Myhill-Nerode equivalence classes:")
        print(
            tabulate(
                [table[cls.word] for cls in equivs],
                headers=table["suffixes"],
                showindex=list(map(lambda x: x.word, equivs)),
                tablefmt="pretty",
            )
        )
    else:
        print(
            (
                "DFA is not minimal. "
                f"It has {len(dfa.useful_states)} states while "
                f"equivalent minimal DFA has {len(equivs)} states."
            )
        )
