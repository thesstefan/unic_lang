import random
from bst import BSTree

def run_test():
    """ Run some quick tests on the BSTree by comparing its behavior
    to a Python dictionary. """

    symbolTable = BSTree()
    pyDict = {}
    
    # Add the same set of key value pairs to a python dictionary and 
    # a BSTree. 
    for _ in range(20): 
        randChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0,25)]
        randInt = random.randint(0,100)
        symbolTable[randInt] = randChar
        pyDict[randInt] = randChar

    # Make sure that symbolTable has the correct length.
    assert len(pyDict) == len(symbolTable)

    # Make sure all elements in pyDict are also in symbolTable
    for key in pyDict:
        assert key in symbolTable
        assert pyDict[key] == symbolTable[key]

    # Make sure all elements in symbolTable are also in pyDict.
    for key in symbolTable:
        assert key in pyDict

    # Remove all items from symbolTable
    for key in pyDict:
        symbolTable.pop(key)

    # Make sure that the size is 0 after all items are removed. 
    assert len(symbolTable) == 0, "size is: " + str(len(symbolTable))

if __name__ == "__main__":
    run_test()
