import argparse
from unic.runners import run_lexer
from unic.runners import run_automata


def arg_parser():
    parser = argparse.ArgumentParser(prog='unic', description='UniC Compiler')
    command_parsers = parser.add_subparsers(help='Command help',
                                            dest='command', required=True)

    lexer_parser = command_parsers.add_parser('lexer',
                                              help='lexer help')
    lexer_parser.add_argument(
            '--use_automata_matching',
            default=True,
            action=argparse.BooleanOptionalAction,
            help='Do identifier and number matching using finite automatas')
    lexer_parser.add_argument(
            '--token_json', default='token.json',
            help='Path to JSON containing tokens split by category')
    lexer_parser.add_argument(
            '--pif_out', default='PIF.out',
            help='Path to file where PIF should be written')
    lexer_parser.add_argument(
            '--symbol_table_out', default='ST.out',
            help='Path to file where the Symbol Table should be written')
    lexer_parser.add_argument(
            'input',
            help='Path to the UniC file to be parsed')

    automata_parser = command_parsers.add_parser('automata',
                                                 help='automata help')
    automata_parser.add_argument('input',
                                 help='Path to automata specification')

    return parser


def main():
    args = vars(arg_parser().parse_args())

    if args['command'] == 'lexer':
        run_lexer(input_path=args['input'],
                  token_json_path=args['token_json'],
                  use_automata_matching=args['use_automata_matching'],
                  symbol_table_out_path=args['symbol_table_out'],
                  pif_out_path=args['pif_out'])

    if args['command'] == 'automata':
        run_automata(input_path=args['input'])


if __name__ == '__main__':
    main()
