import attrs

from typing import Any, Tuple, Optional

from unic.utils.str_map import StrMap, StrMapPosition
from unic.utils.hash_table import HashTable as MapImplementation
from unic.utils.hash_table import HashTablePosition as SymbolTablePosition


@attrs.define
class SymbolTable:
    _map: StrMap = attrs.field(default=attrs.Factory(MapImplementation))

    def at_position(self, position: SymbolTablePosition) -> Tuple[str, Any]:
        return self._map.at_position(position)

    def find_position(self, key: str) -> Optional[StrMapPosition]:
        return self._map.find_position(key)

    def __getitem__(self, key: str) -> int:
        if key not in self._map:
            self._map[key] = None

        return self._map[key]

    def __str__(self) -> str:
        return str(self._map)

    def write_to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write('=== SYMBOL TABLE ===\n\n')

            for key in self._map:
                file.write('{} -> {}\n'.format(
                    self.find_position(key), key))
