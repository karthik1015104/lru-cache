# LRU Cache — From Scratch in Python

A ground-up implementation of a Least Recently Used (LRU) Cache built using a **Doubly Linked List + HashMap**, with a browser simulation, performance analysis, and an optional Streamlit web app.

---

## What is an LRU Cache?

An LRU Cache is a fixed-size data structure that evicts the **least recently used** item when it runs out of space. It is the standard caching strategy used in operating systems, browsers, and databases.

**Core idea:** Every `get` or `put` moves that item to the front. When the cache is full, the item at the back (least recently used) gets evicted.

---

## Project Structure

```
lru-cache/
├── node.py                  # Node class for the doubly linked list
├── doubly_linked_list.py    # DLL with insert_at_front and remove
├── lru_cache.py             # Core LRU Cache logic (HashMap + DLL)
├── main.py                  # Minimal usage example
├── simulation.py            # Browser cache simulation with hit/miss trace
├── analysis.py              # Hit rate vs capacity + speed benchmark plots
├── app.py                   # Streamlit web app (interactive UI)
├── hit_rate_vs_capacity.png # Plot: cache hit rate across capacities 1–15
└── speed_benchmark.png      # Plot: custom DLL vs OrderedDict benchmark
```

---

## How It Works

The cache is built in **four layers**, each adding a level of abstraction:

```
Node  →  DoublyLinkedList  →  LRUCache  →  Applications
```

**Layer 1 — Node (`node.py`)**
A single doubly linked list node holding a `key`, `value`, and `prev`/`next` pointers.

**Layer 2 — DoublyLinkedList (`doubly_linked_list.py`)**
Maintains a list with dummy `head` and `tail` sentinels. Supports O(1) `insert_at_front` and `remove`.

**Layer 3 — LRUCache (`lru_cache.py`)**
Combines a Python `dict` (for O(1) key lookup) with the DLL (for O(1) ordering). Every `get` promotes the node to front. Every `put` inserts at front and evicts the tail node if over capacity.

**Layer 4 — Applications**
- `main.py` — basic correctness demo
- `simulation.py` — browser tab cache with hit/miss trace
- `analysis.py` — performance plots
- `app.py` — interactive Streamlit UI

**Time Complexity:** O(1) for both `get` and `put`
**Space Complexity:** O(capacity)

---

## Quick Start

**Clone the repo**
```bash
git clone https://github.com/karthik1015104/lru-cache.git
cd lru-cache
```

**Run the basic demo**
```bash
python main.py
```

Expected output:
```
A
-1
C
D
```

**Run the browser simulation**
```bash
python simulation.py
```

**Run the performance analysis**
```bash
pip install matplotlib
python analysis.py
```

---

## Browser Cache Simulation

`simulation.py` simulates a sequence of 15 browser page visits with a cache capacity of 4.

```
==================================================
  Browser Cache Simulation (Capacity = 4)
==================================================
  MISS     | Loaded: google.com           | Evicted: None
  MISS     | Loaded: youtube.com          | Evicted: None
  MISS     | Loaded: github.com           | Evicted: None
  HIT      | Accessed: google.com         | Already in cache
  MISS     | Loaded: stackoverflow.com    | Evicted: None
  HIT      | Accessed: github.com         | Already in cache
  HIT      | Accessed: youtube.com        | Already in cache
  MISS     | Loaded: reddit.com           | Evicted: google.com
  MISS     | Loaded: google.com           | Evicted: stackoverflow.com
  MISS     | Loaded: netflix.com          | Evicted: github.com
  MISS     | Loaded: github.com           | Evicted: youtube.com
  MISS     | Loaded: stackoverflow.com    | Evicted: reddit.com
  MISS     | Loaded: twitter.com          | Evicted: google.com
  MISS     | Loaded: google.com           | Evicted: netflix.com
  MISS     | Loaded: reddit.com           | Evicted: github.com
==================================================
  Total Visits : 15
  Cache Hits   : 3
  Cache Misses : 12
  Hit Rate     : 20.0%
==================================================
```

---

## Performance Analysis

### Hit Rate vs Cache Capacity

![Hit Rate vs Capacity](hit_rate_vs_capacity.png)

As capacity increases from 1 to 15, the hit rate rises steadily on the 15-visit browser sequence. The curve plateaus once the cache is large enough to hold all unique pages visited.

### Speed Benchmark — 10,000 Operations

![Speed Benchmark](speed_benchmark.png)

Custom DLL + HashMap implementation benchmarked against Python's built-in `OrderedDict`-based LRU over 10,000 randomised get/put operations (`random.seed(42)`, capacity=20, keys from 1–50).

| Implementation | Approach |
|---|---|
| Custom LRU | Doubly Linked List + HashMap |
| Built-in LRU | `collections.OrderedDict` |

The built-in is faster due to CPython's C-level optimisations for `OrderedDict`. The custom implementation demonstrates the same O(1) algorithmic complexity with pure Python overhead.

---

## Web App (Streamlit)

`app.py` provides an interactive web interface for the LRU Cache. It lets you set capacity, perform get/put operations, and visualise the current cache state in real time.

**To run:**
```bash
pip install streamlit
streamlit run app.py
```

Screenshots:

![Streamlit App 1](streamlit_screenshot_1.png)
![Streamlit App 2](streamlit_screenshot_2.png)

---

## Interview Notes

**Why DLL + HashMap and not just `OrderedDict`?**
`OrderedDict` is a valid production shortcut, but it abstracts away the mechanism. The DLL + HashMap approach makes the O(1) guarantee explicit — pointer rewiring for ordering, hash table for lookup — which is what interviewers and systems design discussions expect.

**Why dummy head and tail sentinels?**
They eliminate all edge cases for inserting into an empty list or removing the only node. No null checks needed inside `insert_at_front` or `remove`.

**Why `put_with_eviction` alongside `put`?**
The simulation layer needs to know *which* key was evicted to display it in the trace. Returning `None` or a key keeps the core cache API clean while exposing eviction info to callers that need it.

---

## Tech Stack

- Python 3.x — no external dependencies for core logic
- Matplotlib — for analysis plots
- Streamlit — for the optional web app

---

## Author

Karthik | [GitHub](https://github.com/karthik1015104)
