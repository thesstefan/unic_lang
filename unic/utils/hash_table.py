import attrs
import itertools

from typing import Any, List, Tuple, Optional, Iterator 
from unic.utils.str_map import StrMap, StrMapPosition


@attrs.define
class HashTableNode:
    key: str
    value: Any

    def __str__(self) -> str:
        return '{}: {}'.format(self.key, self.value)


@attrs.define
class HashTablePosition(StrMapPosition):
    bucket_index: int
    position_in_bucket: int

    def __str__(self) -> str:
        return '({}, {})'.format(self.bucket_index, self.position_in_bucket)


HASH_TABLE_CAPACITY: int = 100


@attrs.define
class HashTable(StrMap):
    size: int = 0
    buckets: List[List[HashTableNode]] = attrs.field(
            default=attrs.Factory(
                lambda: [[] for i in range(HASH_TABLE_CAPACITY)]))

    def _hash(self, key: str) -> int:
        return sum([ord(c) for c in key]) % len(self.buckets)

    def __getitem__(self, key: str) -> Optional[Any]:
        bucket_index = self._hash(key)

        return next((node.value for node in self.buckets[bucket_index]
                    if node.key == key), None)

    def __setitem__(self, key: str, value: Any) -> None:
        position = self.find_position(key)

        if position is None:
            self.buckets[self._hash(key)].append(HashTableNode(key, value))
            self.size += 1

            return

        node = self.buckets[position.bucket_index][position.position_in_bucket]
        node.value = value

    def __contains__(self, key: str) -> bool:
        return self.find_position(key) is not None

    def __len__(self) -> int:
        return self.size

    def items(self) -> List[Tuple[str, Any]]:
        return [(node.key, node.value)
                for node in itertools.chain(*self.buckets)]

    def __iter__(self) -> Iterator[str]:
        yield from (node.key for node in itertools.chain(*self.buckets))

    def __str__(self) -> str:
        return ', '.join((str(item)
                          for item in self.items())).removesuffix(', ')

    def __delitem__(self, key: str) -> None:
        position = self.find_position(key)

        if not position:
            return

        self.size -= 1
        del self.buckets[position.bucket_index][position.position_in_bucket]

    def at_position(self, position: StrMapPosition) -> Tuple[str, Any]:
        assert isinstance(position, HashTablePosition)

        node = self.buckets[position.bucket_index][position.position_in_bucket]

        return node.key, node.value

    def find_position(self, key: str) -> Optional[HashTablePosition]:
        bucket_index = self._hash(key)

        position_in_bucket = next((index for index, node in
                                  enumerate(self.buckets[bucket_index])
                                  if node.key == key), None)

        if position_in_bucket is None:
            return None

        return HashTablePosition(bucket_index, position_in_bucket)
