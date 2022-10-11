import re
from typing import List, Optional

from dfa import DFA


class Parser:
    """Represents a class that performs parsing of the DFA input."""
    
    state_pattern = re.compile(r'[A-Z][0-9]?')
    letter_pattern = re.compile(r'[a-z]')

    def _parse_states(self, line):
        line_splitted = re.split(r'{', line)
        initial_state = self.state_pattern.search(line_splitted[0]).group() # type: ignore
        final_states = self.state_pattern.findall(line_splitted[1])

        return initial_state, set(final_states)

    def _parse_transitions(self, lines):
        states = set()
        alphabet = set()
        transitions = {}
        reversed_transitions = {}

        for line in lines:
            if not line.isspace():
                line_splitted = re.split(r'->', line)
                in_state = self.state_pattern.search(line_splitted[0]).group() # type: ignore
                letter = self.letter_pattern.search(line_splitted[0]).group() # type: ignore
                out_state = self.state_pattern.search(line_splitted[1]).group() # type: ignore
                
                if (in_state, letter) in transitions:
                    return set(), set(), {}, {}, False
                
                states.update({in_state, out_state})
                alphabet.add(letter)
                transitions[in_state, letter] = out_state
                r_out_states = reversed_transitions.get((out_state, letter), set())
                r_out_states.add(in_state)
                reversed_transitions[out_state, letter] = r_out_states

        return states, alphabet, transitions, reversed_transitions, True

    def parse_dfa(self, lines: List[str]) -> Optional[DFA]:
        """Parses input lines and returns DFA if the data is correct."""
        initial_state, final_states = self._parse_states(lines[0])
        (states, alphabet, transitions,
         reversed_transitions, deterministic)  = self._parse_transitions(lines[1:])
        alphabet = sorted(list(alphabet))
        return DFA(states, initial_state, final_states,
                   alphabet, transitions, reversed_transitions) if deterministic else None
