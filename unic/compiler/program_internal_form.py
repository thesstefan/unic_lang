"""Defines PIF data structure."""

import attrs
from typing import List, Tuple


@attrs.define
class ProgramInternalForm:
    """Implementation of PIF data structure."""

    _occurences: List[Tuple[str, str]] = attrs.field(
            default=attrs.Factory(list))

    def push(self, token_or_type: str, position: str) -> None:
        """Adds a new entry to PIF.

        :param token_or_type: A token/type
        :type token_or_type: str

        :param position: Position in SymbolTable
        :type position: int
        """
        self._occurences.append((token_or_type, position))

    def __str__(self) -> str:
        return str(self._occurences)

    def write_to_file(self, file_path: str) -> None:
        """Writes PIF table to file.

        :param file_path: Path to PIF output file
        :type file_path: str
        """
        with open(file_path, 'w') as file:
            file.write('=== PROGRAM INTERNAL FORM ===\n\n')

            for (token_or_type, position) in self._occurences:
                file.write(f'{token_or_type} -> {position}\n')
