# ============================================
# Dictionaries – Check Existence, Iterate & Merge
# ============================================


# ============================================
# Checking Key Existence with 'in'
# ============================================

student = {'name': 'Alice', 'age': 22}

print("--- Key Existence ---")
print("'name' in student:", 'name' in student)     # True
print("'email' in student:", 'email' in student)   # False
print("'name' not in student:", 'name' not in student)  # False

# 'in' checks KEYS only, not values
print("'Alice' in student:", 'Alice' in student)            # False
print("'Alice' in values:", 'Alice' in student.values())    # True


# --- Safe Access Patterns ---

# Pattern 1: Check before access
config = {'port': 8080}
if 'host' not in config:
    config['host'] = 'localhost'
print("\nConfig:", config)

# Pattern 2: .get() for simple fallback
font_size = config.get('font_size', 14)
print(f"Font size: {font_size}")          # 14 (default)

# Pattern 3: try/except (when missing key is unusual)
try:
    value = config['missing_key']
except KeyError:
    value = 'default'
    print(f"Caught KeyError, using: {value}")


# --- Performance ---
# Key lookup with 'in' is O(1) — hash table!
# Much faster than 'in' on a list which is O(n)


# ============================================
# Iterating Through Dictionaries
# ============================================

student = {'name': 'Alice', 'age': 22, 'grade': 'A'}

print("\n--- Iterating Keys (default) ---")
for key in student:
    print(f"  {key}")

print("\n--- Iterating Keys (explicit) ---")
for key in student.keys():
    print(f"  {key}: {student[key]}")

print("\n--- Iterating Values ---")
for value in student.values():
    print(f"  {value}")

print("\n--- Iterating Key-Value Pairs ---")
for key, value in student.items():
    print(f"  {key}: {value}")


# --- Summing Values ---

prices = {'apple': 1.50, 'banana': 0.75, 'cherry': 2.00}
total = sum(prices.values())
print(f"\nTotal price: ${total:.2f}")


# --- Sorted Iteration ---

scores = {'Charlie': 78, 'Alice': 92, 'Bob': 85}

print("\nSorted by key:")
for name in sorted(scores):
    print(f"  {name}: {scores[name]}")

print("\nSorted by value (desc):")
for name in sorted(scores, key=scores.get, reverse=True):
    print(f"  {name}: {scores[name]}")


# --- Dictionary Comprehension (Filter) ---

scores = {'Alice': 92, 'Bob': 45, 'Charlie': 78, 'David': 38}

passing = {name: s for name, s in scores.items() if s >= 50}
print(f"\nPassing students: {passing}")

# Find max/min
top_student = max(scores, key=scores.get)
lowest_student = min(scores, key=scores.get)
print(f"Top student: {top_student} ({scores[top_student]})")
print(f"Lowest: {lowest_student} ({scores[lowest_student]})")


# --- Views Are Live ---

d = {'a': 1, 'b': 2}
keys_view = d.keys()
print(f"\nKeys view before: {list(keys_view)}")

d['c'] = 3
print(f"Keys view after adding 'c': {list(keys_view)}")  # Reflects change!


# --- Never Modify While Iterating ---

# BAD:
# for key in d:
#     if d[key] < 2:
#         del d[key]  # RuntimeError!

# GOOD: Build a new dict
data = {'a': 1, 'b': 5, 'c': 2, 'd': 8}
filtered = {k: v for k, v in data.items() if v >= 3}
print(f"\nFiltered (>= 3): {filtered}")


# ============================================
# Merging Dictionaries
# ============================================

print("\n" + "=" * 40)
print("MERGING DICTIONARIES")
print("=" * 40)

# --- update() — In-Place Merge ---

d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
d1.update(d2)
print(f"\nAfter d1.update(d2): {d1}")    # {'a': 1, 'b': 3, 'c': 4}
# d2's 'b' value (3) overwrites d1's 'b' value (2)


# --- Different Ways to Call update() ---

config = {}
config.update({'port': 8080})              # With dict
config.update(debug=True)                  # With keywords
config.update([('host', 'localhost')])     # With tuples
print(f"Config: {config}")


# --- {**d1, **d2} — Merge Without Modifying ---

defaults = {'debug': False, 'port': 3000}
overrides = {'port': 8080, 'host': 'prod'}

merged = {**defaults, **overrides}
print(f"\nDefaults: {defaults}")          # unchanged
print(f"Overrides: {overrides}")          # unchanged
print(f"Merged: {merged}")               # port=8080 (overrides wins)


# --- | Operator (Python 3.9+) ---

d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

new_dict = d1 | d2          # New dict, originals unchanged
print(f"\nd1 | d2: {new_dict}")

d1 |= d2                    # In-place merge
print(f"d1 |= d2: {d1}")


# --- Config Layering Pattern ---

default_config = {'debug': False, 'port': 3000, 'host': 'localhost'}
env_config = {'port': 8080}
cli_config = {'debug': True}

final_config = {**default_config, **env_config, **cli_config}
print(f"\nFinal config: {final_config}")
# Later dicts win: debug=True (cli), port=8080 (env), host=localhost (default)


# --- Comparison Table ---
# | Method         | Modifies Original? | Python Version |
# |----------------|-------------------|----------------|
# | d1.update(d2)  | Yes               | All            |
# | {**d1, **d2}   | No (new dict)     | 3.5+           |
# | d1 | d2        | No (new dict)     | 3.9+           |
# | d1 |= d2       | Yes               | 3.9+           |

# Note: Merging is SHALLOW — nested dicts are replaced entirely, not deep-merged
