from node import Node
from doubly_linked_list import DoublyLinkedList

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        self.dll = DoublyLinkedList()

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.dll.remove(node)
        self.dll.insert_at_front(node)
        return node.value

    def put(self, key, value):
        if key in self.cache:
            self.dll.remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self.dll.insert_at_front(node)
        if len(self.cache) > self.capacity:
            lru = self.dll.tail.prev
            self.dll.remove(lru)
            del self.cache[lru.key]

    def put_with_eviction(self, key, value):
        evicted = None
        if key in self.cache:
            self.dll.remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self.dll.insert_at_front(node)
        if len(self.cache) > self.capacity:
            lru = self.dll.tail.prev
            self.dll.remove(lru)
            del self.cache[lru.key]
            evicted = lru.key
        return evicted