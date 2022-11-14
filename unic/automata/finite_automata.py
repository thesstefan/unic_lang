import attrs

from typing import Dict, Set, List
from collections import defaultdict


@attrs.define
class State:
    token: str
    final: bool = False
    initial: bool = False
    transitions: Dict[str, List[str]] = attrs.field(
            default=attrs.Factory(lambda: defaultdict(lambda: [])))

    def add_transition(self, destination_state: str, literal: str):
        self.transitions[literal].append(destination_state)

    def is_deterministic(self) -> bool:
        return not any(len(literal_transitions) != 1
                       for literal_transitions in self.transitions.values())

    def __str__(self) -> str:
        return '{}{}Token: {}'.format(
                'Initial, ' if self.initial else '',
                'Final, ' if self.final else '',
                self.token)


@attrs.define
class FiniteAutomata:
    states: Dict[str, State] = attrs.field(default=attrs.Factory(dict))
    alphabet: Set[str] = attrs.field(default=attrs.Factory(set))

    def is_deterministic(self) -> bool:
        return all(state.is_deterministic() for state in self.states.values())

    def add_transition(self,
                       source: str, destination: str, literal: str) -> None:
        if literal not in self.alphabet:
            raise RuntimeError(
                    'Can\'t add transition with invalid alphabet '
                    '-> Unknown literal: {}'.format(literal))

        self.states[source].add_transition(destination, literal)

    def read_from_file(self, file_path: str):
        with open(file_path) as file:
            for literal in map(str.strip, file.readline().split(',')):
                self.alphabet.add(literal)

            for state in map(str.strip, file.readline().split(',')):
                self.states[state] = State(state)

            initial_state = file.readline().strip()
            self.states[initial_state].initial = True

            for final_state in map(str.strip, file.readline().split(',')):
                self.states[final_state].final = True

            while transition := file.readline():
                source, literal, destination = map(str.strip,
                                                   transition.split(','))

                self.add_transition(source, destination, literal)

    def accept(self, word):
        current_state = next(filter(lambda state: state.initial,
                                    self.states.values()))

        for symbol in word:
            if symbol not in current_state.transitions.keys():
                return False

            current_state = self.states[current_state.transitions[symbol][0]]

        return current_state.final
