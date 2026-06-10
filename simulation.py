from lru_cache import LRUCache

# Simulated sequence of page visits
visits = [
    "google.com", "youtube.com", "github.com", "google.com",
    "stackoverflow.com", "github.com", "youtube.com", "reddit.com",
    "google.com", "netflix.com", "github.com", "stackoverflow.com",
    "twitter.com", "google.com", "reddit.com"
]

# Cache capacity — only remembers 4 pages at a time
CAPACITY = 4

def run_simulation():
    cache = LRUCache(CAPACITY)
    hits = 0
    misses = 0

    print("=" * 50)
    print(f"  Browser Cache Simulation (Capacity = {CAPACITY})")
    print("=" * 50)

    for page in visits:
        result = cache.get(page)

        if result == -1:
            # Miss — page not in cache
            misses += 1
            evicted = cache.put_with_eviction(page, page)
            if evicted:
                print(f"  MISS     | Loaded: {page:<20} | Evicted: {evicted}")
            else:
                print(f"  MISS     | Loaded: {page:<20} | Evicted: None")
        else:
            # Hit — page already in cache
            hits += 1
            print(f"  HIT      | Accessed: {page:<18} | Already in cache")

    print("=" * 50)
    print(f"  Total Visits : {len(visits)}")
    print(f"  Cache Hits   : {hits}")
    print(f"  Cache Misses : {misses}")
    print(f"  Hit Rate     : {round((hits / len(visits)) * 100, 2)}%")
    print("=" * 50)

run_simulation()