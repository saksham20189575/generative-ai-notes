# ============================================
# Slicing – Extract Portions of Lists
# ============================================


# --- Basic Slicing [start:stop] ---

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print("Original:", numbers)
print("numbers[2:7]:", numbers[2:7])     # [2, 3, 4, 5, 6]
print("numbers[0:5]:", numbers[0:5])     # [0, 1, 2, 3, 4]
print("numbers[3:6]:", numbers[3:6])     # [3, 4, 5] (stop is exclusive!)


# --- Omitting Start and Stop ---

data = [10, 20, 30, 40, 50, 60, 70]

print("\nOmitting start/stop:")
print("data[:4]:", data[:4])             # [10, 20, 30, 40]  (first 4)
print("data[3:]:", data[3:])             # [40, 50, 60, 70]  (from index 3)
print("data[:]:", data[:])               # full copy


# --- Negative Indices ---

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("\nNegative indices:")
print("items[-3:]:", items[-3:])         # [8, 9, 10]  (last 3)
print("items[:-2]:", items[:-2])         # [1..8]  (all except last 2)
print("items[2:-2]:", items[2:-2])       # [3, 4, 5, 6, 7, 8]
print("items[-5:-2]:", items[-5:-2])     # [6, 7, 8]


# --- Step Parameter ---

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print("\nStep parameter:")
print("every 2nd:", numbers[::2])        # [0, 2, 4, 6, 8]
print("every 3rd:", numbers[::3])        # [0, 3, 6, 9]
print("odd indices:", numbers[1::2])     # [1, 3, 5, 7, 9]
print("range 1-8 step 2:", numbers[1:8:2])  # [1, 3, 5, 7]


# --- Negative Step (Reverse) ---

print("\nReversing:")
print("reversed:", numbers[::-1])        # [9, 8, 7, ..., 0]
print("reverse step 2:", numbers[::-2])  # [9, 7, 5, 3, 1]


# --- Slice Assignment ---

print("\nSlice assignment:")

# Replace a portion
nums = [1, 2, 3, 4, 5]
nums[1:3] = [20, 30]
print("Replace [1:3]:", nums)            # [1, 20, 30, 4, 5]

# Delete via empty list
nums = [1, 2, 3, 4, 5]
nums[1:3] = []
print("Delete [1:3]:", nums)             # [1, 4, 5]

# Insert via empty slice
nums = [1, 2, 5]
nums[2:2] = [3, 4]
print("Insert at [2:2]:", nums)          # [1, 2, 3, 4, 5]

# Replace with different length
nums = [1, 2, 3, 4, 5]
nums[1:3] = [20, 30, 40, 50]
print("Diff length:", nums)              # [1, 20, 30, 40, 50, 4, 5]


# --- Common Patterns ---

print("\nCommon patterns:")

# Split list in half
data = [1, 2, 3, 4, 5, 6, 7, 8]
mid = len(data) // 2
first_half = data[:mid]
second_half = data[mid:]
print("First half:", first_half)         # [1, 2, 3, 4]
print("Second half:", second_half)       # [5, 6, 7, 8]

# Remove first and last
items = ['start', 'a', 'b', 'c', 'end']
core = items[1:-1]
print("Core (no first/last):", core)     # ['a', 'b', 'c']

# Shallow copy
original = [1, 2, 3]
copy = original[:]
copy.append(4)
print("Original:", original)             # [1, 2, 3] (unchanged)
print("Copy:", copy)                     # [1, 2, 3, 4]

# Palindrome check
word = list("racecar")
print("Is palindrome:", word == word[::-1])  # True


# --- Processing Chunks ---

print("\nProcessing in chunks of 5:")
data = list(range(20))
chunk_size = 5

for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    print(f"  Chunk: {chunk}")
