import attrs
from unic.utils.bst import BSTree


@attrs.define
class SymbolTable:
    _tree: BSTree = attrs.field(default=attrs.Factory(BSTree))
    _current_index: int = 0

    def __getitem__(self, key: str) -> int:
        if key in self._tree:
            return self._tree[key]

        self._tree[key] = self._current_index
        self._current_index += 1

        return self._tree[key]

    def __str__(self) -> str:
        return str(self._tree)

    def write_to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write('=== SYMBOL TABLE ===\n\n')

            for node in self._tree:
                file.write(f'{node} -> {self._tree[node]}\n')
