from lru_cache import LRUCache

lru = LRUCache(3)

lru.put(1, "A")
lru.put(2, "B")
lru.put(3, "C")
print(lru.get(1))   # should print A

lru.put(4, "D")     # evicts 2
print(lru.get(2))   # should print -1
print(lru.get(3))   # should print C
print(lru.get(4))   # should print D