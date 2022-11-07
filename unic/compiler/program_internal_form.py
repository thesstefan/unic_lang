import attrs
from typing import List, Tuple


@attrs.define
class ProgramInternalForm:
    _occurences: List[Tuple[str, int]] = attrs.field(default=attrs.Factory(list))

    def push(self, token_or_type: str, position: int) -> None:
        self._occurences.append((token_or_type, position))

    def __str__(self) -> str:
        return str(self._occurences)

    def write_to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write('=== PROGRAM INTERNAL FORM ===\n\n')

            for (token_or_type, position) in self._occurences:
                file.write(f'{token_or_type} -> {position}\n')
