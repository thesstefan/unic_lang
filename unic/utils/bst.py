import random
import attrs

class _BSTNode(object):
    """ Private storage class for the BSTree. """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.key) + ": " + str(self.value) 


class BSTree(object):
    """ 
    A binary search tree implementation of the Symbol Table.  This class
    implements a subset of the functionality provided by the built-in
    Python dictionary class.
    """
    
    def __init__(self):
        """ Construct an empty symbol table. """
        self._root = None
        self._size = 0

    def __len__(self):
        """ Return the number of values stored in the symbol table."""
        return self._size
    
    def __contains__(self, key):
        """ Return true if key is in the symbol table, False otherwise """
        return not self._findNode(self._root, key) is None

    def __getitem__(self, key):
        """ 
        Return the value associtated with key. Raises a KeyError
        if key is not in the symbol table. 
        """
        node = self._findNode(self._root, key)
        if node == None:
            raise KeyError()
        return node.value

    def get(self, key):
        """ 
        Return the value associtated with key. Returns None if key is not
        in the symbol table. 
        """
        node = self._findNode(self._root, key)
        if node == None:
            return None
        else:
            return node.value

    def _findNode(self, subtree, key):
        # Recursive helper method for __getitem__ and __contains__. 
        # Returns the _BSTNode that contains key, or None if key is not
        # in the map. 
        if subtree == None:
            return None
        elif subtree.key == key:
            return subtree
        elif subtree.key < key:
            return self._findNode(subtree.right, key)
        else:
            return self._findNode(subtree.left, key)
        
    def __setitem__(self, key, value):
        """ Implements self[key] = value.  If key is already stored in
        the symbol table then its value is modified.  If key is not in the table,
        it is added."""

        if self._root == None:
            self._root = _BSTNode(key, value)
            self._size += 1
        else:
            self._setItem(self._root, key, value)
        
    def _setItem(self, subtree, key, value):
        # Internal helper method for __setitem__.

        assert subtree is not None

        # The key has been found: 
        if subtree.key == key:
            subtree.value = value

        # The key belongs on the left: 
        elif key < subtree.key:
            if subtree.left is None:
                subtree.left = _BSTNode(key, value)
                self._size += 1
            else:
                self._setItem(subtree.left, key, value)

        #The key belongs on the right: 
        else:
            if subtree.right is None:
                subtree.right = _BSTNode(key, value)
                self._size += 1
            else:
                self._setItem(subtree.right, key, value)
   
    def __str__(self):
        """ Return the symbol table as a string. """
        result = "{"
        for key in self:
            result += str(key) + ": " + str(self[key]) + ", "
        result = result.rstrip(", ")
        return result + "}"
        

    def __iter__(self):
        """ Return an in-order iterator over keys. """
        return _InorderBSTIterator(self._root)

    def _height(self, subtree):
        # Recursively calculate the height of the subtree. 
        # (Needed for the tree drawing method.)
        if subtree is None: 
            return 0
        else:
            return 1 + max(self._height(subtree.left),
                           self._height(subtree.right))

    def pop(self, key):
        """ Remove and return the value with the indicated key.
        Raise a KeyError if the key is not in the symbol table."""
        value = self[key]
        self._root = self._bstRemove(self._root, key)
        self._size -= 1
        return value

    def _bstRemove(self, subtree, key):
        # Recursively remove the node containing key from this subtree.
        # 
        # This method works by returning a modified version of the current
        # subtree that does not contain the indicated key. 
        #
        # Precondition: key is in the subtree. 
        # Returns: A _BSTNode, or None if this is a leaf that is
        #          is being removed. 
        #
        assert subtree is not None, "Cannot remove non-existent key."

        # Key is in the left subtree: 
        if key < subtree.key:
            subtree.left = self._bstRemove(subtree.left, key)
            return subtree
        
        # Key is in the right subtree: 
        elif key > subtree.key:
            subtree.right = self._bstRemove(subtree.right, key)
            return subtree

        # The key has been located at the current node: 
        else:
            # This is a leaf node: 
            if subtree.left is None and subtree.right is None:
                return None

            # Only a left child:
            elif subtree.left is not None and subtree.right is None:
                return subtree.left

            # Only a right child:
            elif subtree.left is None and subtree.right is not None:
                return subtree.right

            # Two children:
            else:
                successor = self._bstMinimum(subtree.right)
                subtree.key = successor.key
                subtree.value = successor.value
                subtree.right = self._bstRemove(subtree.right, successor.key)
                return subtree
                
    def _bstMinimum(self, subtree):
        # Return the mininum node in this subtree by recursively following
        # left children. 
        if subtree is None:
            return None
        if subtree.left is None:
            return subtree
        else:
            return self._bstMinimum(subtree.left)


class _InorderBSTIterator(object):
    # Inorder Iterator class.  Traversal state is maintained between
    # calls using a stack.

    def __init__(self, root):
        self.stack = []
        curNode = root

        # Keep pushing left children onto the stack.  After this, the
        # top node on the stack will be the leftmost node in the tree.
        # That will be the first item visited in an inorder traversal.

        while curNode is not None:
            self.stack.append(curNode)
            curNode = curNode.left
        
    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration()
        
        # The current node is at the top of the stack. 

        curNode = self.stack.pop()
        key = curNode.key

        # The next item that should be visited is the left-most node
        # in the right subtree.

        if curNode.right is not None:
            self.stack.append(curNode.right)

            curNode = curNode.right.left
            while curNode is not None:
                self.stack.append(curNode)
                curNode = curNode.left

        return key
