import time
import random
import matplotlib.pyplot as plt
from collections import OrderedDict
from lru_cache import LRUCache

random.seed(42)  # for reproducibility

# ── Shared visit sequence ─────────────────────────────────────────
pages = [
    "google.com", "youtube.com", "github.com", "google.com",
    "stackoverflow.com", "github.com", "youtube.com", "reddit.com",
    "google.com", "netflix.com", "github.com", "stackoverflow.com",
    "twitter.com", "google.com", "reddit.com"
]

# ── Section 1: Hit Rate vs Capacity ──────────────────────────────
def get_hit_rate(capacity, visits):
    cache = LRUCache(capacity)
    hits = 0
    for page in visits:
        if cache.get(page) != -1:
            hits += 1
        else:
            cache.put(page, page)
    return round((hits / len(visits)) * 100, 2)

capacities = list(range(1, 16))
hit_rates = [get_hit_rate(c, pages) for c in capacities]

plt.figure(figsize=(8, 4))
plt.plot(capacities, hit_rates, marker="o", color="royalblue", linewidth=2)
plt.title("Hit Rate vs Cache Capacity")
plt.xlabel("Cache Capacity")
plt.ylabel("Hit Rate (%)")
plt.xticks(capacities)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("hit_rate_vs_capacity.png")
plt.show()
print("Plot 1 saved: hit_rate_vs_capacity.png")

# ── Section 2: Speed Benchmark ────────────────────────────────────

# Built-in OrderedDict based LRU
class BuiltinLRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Generate 10,000 random operations
keys = [str(random.randint(1, 50)) for _ in range(10000)]

# Benchmark custom LRU
custom = LRUCache(20)
start = time.perf_counter()
for key in keys:
    if custom.get(key) == -1:
        custom.put(key, key)
custom_time = time.perf_counter() - start

# Benchmark built-in LRU
builtin = BuiltinLRU(20)
start = time.perf_counter()
for key in keys:
    if builtin.get(key) == -1:
        builtin.put(key, key)
builtin_time = time.perf_counter() - start

print(f"\nCustom LRU  : {round(custom_time * 1000, 4)} ms")
print(f"Builtin LRU : {round(builtin_time * 1000, 4)} ms")

plt.figure(figsize=(6, 4))
plt.bar(["Custom LRU\n(DLL + HashMap)", "Built-in LRU\n(OrderedDict)"],
        [custom_time * 1000, builtin_time * 1000],
        color=["royalblue", "darkorange"],
        width=0.4)
plt.title("Speed Benchmark — 10,000 Operations")
plt.ylabel("Time (ms)")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("speed_benchmark.png")
plt.show()
print("Plot 2 saved: speed_benchmark.png")
