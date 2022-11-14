import random

from unic.utils.str_map import StrMap
from unic.utils.bst import BSTMap
from unic.utils.hash_table import HashTable

from typing import Type


def run_test(map_type: Type[StrMap]):
    """ Run some quick tests on the BSTree by comparing its behavior
    to a Python dictionary. """

    map_container = map_type()
    pyDict = {}

    # Add the same set of key value pairs to a python dictionary and
    # a BSTree.
    for _ in range(20):
        randChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0, 25)]
        randInt = random.randint(0, 100)
        map_container[str(randInt)] = randChar
        pyDict[str(randInt)] = randChar

    # Make sure that map_container has the correct length.
    assert len(pyDict) == len(map_container)

    # Make sure all elements in pyDict are also in map_container
    for key in pyDict:
        assert key in map_container
        assert pyDict[key] == map_container[key]

    # Make sure all elements in map_container are also in pyDict.
    for key in map_container:
        assert key in pyDict

    # Remove all items from map_container
    for key in pyDict:
        del map_container[key]

    # Make sure that the size is 0 after all items are removed.
    assert len(map_container) == 0, "size is: " + str(len(map_container))


if __name__ == "__main__":
    run_test(BSTMap)
    run_test(HashTable)
