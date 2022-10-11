from dataclasses import dataclass
from queue import Queue
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class DFA:
    """Represents deterministic finite automaton."""

    states: Set[str]
    initial_state: str
    final_states: Set[str]
    alphabet: List[str]
    transitions: Dict[Tuple[str, str], str]
    reversed_transitions: Dict[Tuple[str, str], Set[str]]

    def __post_init__(self):
        self.useful_states = self._get_reachable_states() & self._get_undead_states()
        self.memoized_accepts = {}

    def _get_reachable_from(self, start_states, transitions):
        reachable = start_states.copy()
        states_to_visit = Queue()

        for state in reachable:
            states_to_visit.put(state)

        def update(state):
            if state not in reachable:
                states_to_visit.put(state)
                reachable.add(state)

        while not states_to_visit.empty():
            in_state = states_to_visit.get()
            for letter in self.alphabet:
                out_states = transitions.get((in_state, letter), None)
                if isinstance(out_states, str):
                    update(out_states)
                elif isinstance(out_states, set):
                    for out_state in out_states:
                        update(out_state)

        return reachable

    def _get_reachable_states(self):
        return self._get_reachable_from({self.initial_state}, self.transitions)

    def _get_undead_states(self):
        return self._get_reachable_from(self.final_states, self.reversed_transitions)

    def reach_from_state(self, state, word):
        """Returns state that can be reached from the given state by the given word."""
        for letter in word:
            state = self.transitions.get((state, letter), None)
            if not state or state not in self.useful_states:
                return None
        return state

    def accepts(self, word: str) -> bool:
        """Checks whether the DFA accepts given word."""
        if word not in self.memoized_accepts:
            self.memoized_accepts[word] = (
                self.reach_from_state(self.initial_state, word) in self.final_states
            )

        return self.memoized_accepts[word]

    def sync_from_word(self, word: str) -> Optional[str]:
        """Returns the state to which the word synchronizes the DFA."""
        sync_state = self.reach_from_state(self.initial_state, word)
        return (
            sync_state
            if all(
                sync_state == self.reach_from_state(state, word)
                for state in self.useful_states
            )
            else None
        )
