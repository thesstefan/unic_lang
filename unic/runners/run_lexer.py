from unic.compiler.parser import Parser, ParserError
import sys


def run_lexer(input_path: str,
              token_json_path: str,
              use_automata_matching: bool,
              symbol_table_out_path: str,
              pif_out_path: str) -> None:
    parser = Parser(token_json_path, use_automata_matching)

    try:
        symbol_table, pif = parser.parse_file(input_path)

        symbol_table.write_to_file(symbol_table_out_path)
        pif.write_to_file(pif_out_path)
    except ParserError as e:
        print(e, file=sys.stderr)

        return

    print(f"LEXER: Parsed {input_path} succesfully.")
