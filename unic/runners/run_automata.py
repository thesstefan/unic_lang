from unic.automata.finite_automata import FiniteAutomata


def run_automata(input_path: str) -> None:
    running = True

    automata = FiniteAutomata()
    automata.read_from_file(input_path)
    deterministic = automata.is_deterministic()

    while running:
        print('''
            === FINITE AUTOMATA ===

            1. Show states
            2. Show alphabet
            3. Show transitions
            4. Show initial
            5. Show final
            6. Match pattern
            0. Exit
        ''')

        choice = input('Your choice: ')

        match choice:
            case '1':
                for state in automata.states.values():
                    print(state)

            case '2':
                for terminal_symbol in automata.alphabet:
                    print(terminal_symbol)
            case '3':
                for state in automata.states.values():
                    for literal, dest_states, in state.transitions.items():
                        for destination_state in dest_states:
                            print('{}, {}, {}'.format(
                                state.token, literal, destination_state))
            case '4':
                print(next(
                    filter(lambda state: state.initial,
                           automata.states.values())))
            case '5':
                for final_state in filter(lambda state: state.final,
                                          automata.states.values()):
                    print(final_state)
            case '6':
                if not deterministic:
                    continue

                text = input('Text: ')
                print(automata.accept(text))
            case '0':
                print('Exitting...')

                running = False
            case _:
                print('Invalid choice. Try again!')
