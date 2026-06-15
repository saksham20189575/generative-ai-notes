# ============================================
# Lists – Built-in Functions & Common Methods
# ============================================


# ============================================
# Built-in Functions (work on any iterable)
# ============================================

nums = [3, 1, 4, 1, 5, 9, 2, 6]
print("nums:", nums)

# --- len() ---
print(f"\nlen(nums): {len(nums)}")           # 8

# --- sum() ---
print(f"sum(nums): {sum(nums)}")             # 31

# --- max() / min() ---
print(f"max(nums): {max(nums)}")             # 9
print(f"min(nums): {min(nums)}")             # 1

# --- sorted() — Returns NEW sorted list ---
sorted_nums = sorted(nums)
print(f"\nsorted(nums): {sorted_nums}")       # [1, 1, 2, 3, 4, 5, 6, 9]
print(f"original nums: {nums}")              # unchanged!

# Reverse sort
desc = sorted(nums, reverse=True)
print(f"sorted(reverse=True): {desc}")

# --- reversed() — Iterator in reverse ---
rev = list(reversed(nums))
print(f"\nreversed: {rev}")

# --- enumerate() — (index, value) pairs ---
fruits = ['apple', 'banana', 'cherry']

print("\nenumerate:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

print("\nenumerate (start=1):")
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}. {fruit}")

# --- zip() — Walk lists in parallel ---
names = ['Alice', 'Bob', 'Charlie']
scores = [92, 85, 78]

print("\nzip:")
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

# Create dict from zip
student_scores = dict(zip(names, scores))
print(f"dict(zip): {student_scores}")


# ============================================
# Common List Methods (mutate in place)
# ============================================

print("\n" + "=" * 40)
print("LIST METHODS")
print("=" * 40)

# --- append(x) — Add one element at end ---
items = [1, 2, 3]
items.append(4)
print(f"\nappend(4): {items}")               # [1, 2, 3, 4]

# --- extend(iter) — Add all items from iterable ---
items.extend([5, 6])
print(f"extend([5,6]): {items}")             # [1, 2, 3, 4, 5, 6]

# --- insert(i, x) — Insert at index ---
items.insert(0, 0)
print(f"insert(0, 0): {items}")              # [0, 1, 2, 3, 4, 5, 6]

# --- pop() / pop(i) — Remove & return ---
last = items.pop()
print(f"\npop(): {last}, list: {items}")      # 6, [0, 1, 2, 3, 4, 5]

second = items.pop(1)
print(f"pop(1): {second}, list: {items}")    # 1, [0, 2, 3, 4, 5]

# --- remove(x) — Remove first occurrence ---
items = [2, 3, 2, 4, 2]
items.remove(2)
print(f"\nremove(2): {items}")               # [3, 2, 4, 2] (only first 2 removed)

# --- sort() — Sort in place (returns None) ---
nums = [3, 1, 4, 1, 5]
result = nums.sort()
print(f"\nsort(): {nums}")                   # [1, 1, 3, 4, 5]
print(f"sort() returns: {result}")           # None!

# Reverse sort
nums.sort(reverse=True)
print(f"sort(reverse=True): {nums}")         # [5, 4, 3, 1, 1]

# --- reverse() — Reverse in place ---
items = [1, 2, 3, 4, 5]
items.reverse()
print(f"\nreverse(): {items}")               # [5, 4, 3, 2, 1]

# --- count(x) — Count occurrences ---
nums = [1, 2, 2, 3, 3, 3]
print(f"\ncount(3): {nums.count(3)}")        # 3
print(f"count(1): {nums.count(1)}")          # 1

# --- index(x) — Find index of first x ---
items = ['a', 'b', 'c', 'b']
print(f"\nindex('b'): {items.index('b')}")   # 1 (first occurrence)
# items.index('z')  # ValueError if not found


# ============================================
# Key Difference: sorted() vs .sort()
# ============================================

print("\n--- sorted() vs .sort() ---")

original = [3, 1, 4, 1, 5]

# sorted() — returns NEW list, original unchanged
new_list = sorted(original)
print(f"sorted(): {new_list}")
print(f"original: {original}")              # unchanged

# .sort() — sorts IN PLACE, returns None
original.sort()
print(f"\n.sort(): {original}")              # sorted now
# Can't do: new = original.sort()  — that gives None!


# ============================================
# Practical Examples
# ============================================

print("\n--- Practical Examples ---")

# Find top 3 scores
scores = [72, 95, 88, 64, 91, 83, 97]
top_3 = sorted(scores, reverse=True)[:3]
print(f"Top 3 scores: {top_3}")

# Count and find unique
nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(nums))
print(f"Unique values: {sorted(unique)}")
print(f"Most frequent: {max(set(nums), key=nums.count)}")

# Pair names with ranks
names = ['Alice', 'Bob', 'Charlie']
for rank, name in enumerate(sorted(names), start=1):
    print(f"  #{rank}: {name}")
