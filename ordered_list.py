class Node:
    '''Node for use with doubly-linked list'''

    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None


class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = Node("dummy")
        self.head.next = self.head
        self.head.prev = self.head

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next == self.head

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  Assume that all items added to your
           list can be compared using the < operator and can be compared for equality/inequality.
           Make no other assumptions about the items in your list'''
        new = Node(item)
        if self.is_empty() or self.head.prev.item < new.item:
            new.next = self.head
            new.prev = self.head.prev
            self.head.prev.next = new
            self.head.prev = new
            return True
        else:
            current = self.head.next
            while current.item < new.item:
                current = current.next
            if current.item == new.item:
                return False
            new.next = current
            new.prev = current.prev
            current.prev.next = new
            current.prev = new
            return True

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list)
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        remove = Node(item)
        current = self.head.next
        while remove.item != current.item and current != self.head:
            current = current.next
        if remove.item == current.item:
            current.prev.next = current.next
            current.next.prev = current.prev
            return True
        return False

    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        current = self.head.next
        index = 0
        while item != current.item and current != self.head:
            current = current.next
            index += 1
        if item == current.item:
            return index
        return None

    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if index < 0 or index >= self.size():
            raise IndexError
        current = self.head.next
        if index == 0:
            self.head.next = current.next
            current.next.prev = self.head  #might be a problem
            return current.item
        for i in range(index):
            current = current.next
        current.prev.next = current.next
        current.next.prev = current.prev
        return current.item

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.search_helper(self.head.next, item)

    def search_helper(self, node, item):
        if node == self.head:
            return False
        if node.item == item:
            return True
        return self.search_helper(node.next, item)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        if self.is_empty():
            return []
        current = self.head.next
        result = []
        while current != self.head:
            result.append(current.item)
            current = current.next
        return result

    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        if self.is_empty():
            return []
        current = self.head.prev
        result = []
        return self.python_list_reversed_helper(current, result)

    def python_list_reversed_helper(self, node, result):
        if node == self.head:
            return result
        result.append(node.item)
        return self.python_list_reversed_helper(node.prev, result)


    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.head.next)

    def size_helper(self, node):
        if node == self.head:
            return 0
        return 1 + self.size_helper(node.next)
