"""Defines parser used to analyze the lexic of UniC."""

from unic.compiler.symbol_table import SymbolTable
from unic.compiler.program_internal_form import ProgramInternalForm

import json
import attrs
import re
import itertools
from enum import Enum
from typing import List, Dict

TokenType = Enum('TokenType',
                 ['KEYWORD', 'OPERATOR', 'DELIMITER', 'IDENTIFIER',
                  'INT_CONSTANT', 'STR_CONSTANT', 'UNKNOWN'])


class ParserError(RuntimeError):
    """Exception thrown by Parser if passed code is not lexically correct."""
    pass


@attrs.define
class Parser:
    """Class that parses UniC code and constructs the
    corresponding PIF and SymbolTable.

    :ivar token_json_path: Path to file containing UniC tokens by category.
    """
    token_json_path: str
    _tokens_by_type: Dict[str, List[str]] = attrs.field(
            default=attrs.Factory(dict))

    def _populate_tokens(self, token_json_path: str) -> None:
        with open(token_json_path) as token_json_file:
            self._tokens_by_type = json.load(token_json_file)

    def __attrs_post_init__(self) -> None:
        self._populate_tokens(self.token_json_path)

    def _token_type(self, token: str) -> TokenType:
        if token in self._tokens_by_type['keyword']:
            return TokenType.KEYWORD

        if token in self._tokens_by_type['operator']:
            return TokenType.OPERATOR

        if token in self._tokens_by_type['delimiter']:
            return TokenType.DELIMITER

        identifier_pattern = '[_a-zA-Z][_a-zA-Z0-9]*'
        if re.fullmatch(identifier_pattern, token):
            return TokenType.IDENTIFIER

        string_literal_pattern = '\"(\\.|[^\"])*\"'
        if re.fullmatch(string_literal_pattern, token):
            return TokenType.STR_CONSTANT

        number_pattern = '[1-9][0-9]*|0'
        if re.fullmatch(number_pattern, token):
            return TokenType.INT_CONSTANT

        return TokenType.UNKNOWN

    def _setup_token_for_regex(self, token: str) -> str:
        return token.replace('||', '|\|').replace('&&', '&\&')

    def _discovered_tokens_by_line(self,
                                   file_path: str) -> Dict[int, List[str]]:
        with open(file_path) as file:
            code_lines = file.read().splitlines()

        token_list = list(itertools.chain.from_iterable(
                            self._tokens_by_type.values()))
        token_pattern = '|'.join(
            # TODO: Horrible, fix this
            token if token in self._tokens_by_type['keyword']
            else f'\{self._setup_token_for_regex(token)}'
            for token in token_list)

        discovered_tokens_by_line: Dict[int, List[str]] = {}
        for line, code in enumerate(code_lines):
            tokens = [token.strip() for token in
                      re.split(rf'({token_pattern})', code) if token.strip()]

            discovered_tokens_by_line[line] = tokens

        return discovered_tokens_by_line

    def parse_file(self, file_path: str):
        """Takes an UniC file path and parses it, returning the corresponding
        SymbolTable and PIF.

        :param file_path: Path of file containing UniC code
        :type file_path: str

        :raises ParserError: If given UniC code is not lexically correct.

        :returns: Corresponding SymbolTable and ProgramInternalForm
        :rtype: (SymbolTable, ProgramInternalForm)
        """
        discovered_tokens_by_line = self._discovered_tokens_by_line(file_path)

        pif = ProgramInternalForm()
        symbol_table = SymbolTable()

        for line in discovered_tokens_by_line.keys():
            for token in discovered_tokens_by_line[line]:
                token_type = self._token_type(token)

                if token_type == TokenType.UNKNOWN:
                    raise ParserError('LEXER: Lexical error on #{line}: '
                                      f'Invalid token -> {token}')

                if token_type in [TokenType.KEYWORD,
                                  TokenType.OPERATOR,
                                  TokenType.DELIMITER]:
                    pif.push(token, '-1')
                else:
                    symbol_table[token]
                    pif.push(token_type.name,
                             str(symbol_table.find_position(token)))

        return symbol_table, pif
