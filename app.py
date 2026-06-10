import streamlit as st
from lru_cache import LRUCache

st.set_page_config(page_title="LRU Cache Visualizer", layout="centered")
st.title("🗂️ LRU Cache Visualizer")
st.markdown("Simulate a browser history cache — see hits, misses, and evictions in real time.")

# ── Sidebar controls ──────────────────────────────────────────────
st.sidebar.header("Cache Settings")
capacity = st.sidebar.slider("Cache Capacity", min_value=2, max_value=10, value=4)

# Reset cache if capacity changes
if "capacity" not in st.session_state or st.session_state.capacity != capacity:
    st.session_state.capacity = capacity
    st.session_state.cache = LRUCache(capacity)
    st.session_state.log = []
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.cache_order = []

# ── Page visit input ──────────────────────────────────────────────
st.subheader("Visit a Page")
page = st.text_input("Enter a page name (e.g. google.com)", key="page_input")

if st.button("Visit"):
    if page.strip() == "":
        st.warning("Please enter a page name.")
    else:
        cache = st.session_state.cache
        result = cache.get(page)

        if result == -1:
            evicted = cache.put_with_eviction(page, page)
            st.session_state.misses += 1
            if evicted:
                log_entry = f"❌ MISS  |  Loaded: {page}  |  Evicted: {evicted}"
            else:
                log_entry = f"❌ MISS  |  Loaded: {page}  |  Evicted: None"
        else:
            st.session_state.hits += 1
            log_entry = f"✅ HIT   |  Accessed: {page}  |  Already in cache"

        st.session_state.log.append(log_entry)

        # Rebuild cache order from MRU to LRU
        order = []
        node = cache.dll.head.next
        while node != cache.dll.tail:
            order.append(node.key)
            node = node.next
        st.session_state.cache_order = order

# ── Cache state display ───────────────────────────────────────────
st.subheader("Cache State")
if st.session_state.cache_order:
    for i, key in enumerate(st.session_state.cache_order):
        if i == 0:
            st.success(f"🟢 MRU  →  {key}")
        elif i == len(st.session_state.cache_order) - 1:
            st.error(f"🔴 LRU  →  {key}  (evicted next)")
        else:
            st.info(f"🔵        {key}")
else:
    st.write("Cache is empty. Start visiting pages.")

# ── Stats ─────────────────────────────────────────────────────────
st.subheader("Stats")
total = st.session_state.hits + st.session_state.misses
hit_rate = round((st.session_state.hits / total) * 100, 2) if total > 0 else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Hits", st.session_state.hits)
col2.metric("Misses", st.session_state.misses)
col3.metric("Hit Rate", f"{hit_rate}%")

# ── Log ───────────────────────────────────────────────────────────
st.subheader("Visit Log")
if st.session_state.log:
    for entry in reversed(st.session_state.log):
        st.text(entry)
else:
    st.write("No visits yet.")

# ── Reset button ──────────────────────────────────────────────────
if st.button("Reset Cache"):
    st.session_state.cache = LRUCache(capacity)
    st.session_state.log = []
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.cache_order = []