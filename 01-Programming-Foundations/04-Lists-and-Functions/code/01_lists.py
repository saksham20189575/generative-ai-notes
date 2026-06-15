# ============================================
# Lists – Create, Initialize & Access Elements
# ============================================


# --- Creating Empty Lists ---

empty1 = []
empty2 = list()

if not empty1:
    print("List is empty")


# --- Lists with Initial Values ---

numbers = [1, 2, 3, 4, 5]
fruits = ['apple', 'banana', 'orange']
prices = [19.99, 29.99, 9.99]

# Mixed types allowed
student = ['Alice', 21, 3.8, True]

# Duplicates allowed
nums = [1, 2, 2, 3, 3, 3]

print("numbers:", numbers)
print("fruits:", fruits)
print("student:", student)


# --- Creating from range() ---

nums_from_range = list(range(10))       # [0, 1, 2, ..., 9]
evens = list(range(2, 11, 2))           # [2, 4, 6, 8, 10]

print("range(10):", nums_from_range)
print("evens:", evens)


# --- Creating from Strings ---

chars = list("hello")                   # ['h', 'e', 'l', 'l', 'o']
words = "a b c".split()                 # ['a', 'b', 'c']
items = "x,y,z".split(',')             # ['x', 'y', 'z']

print("chars:", chars)
print("words:", words)
print("items:", items)


# --- Special Patterns ---

zeros = [0] * 5                         # [0, 0, 0, 0, 0]
combined = [1, 2] + [3, 4]             # [1, 2, 3, 4]

print("zeros:", zeros)
print("combined:", combined)


# --- Nested Lists (Matrices) ---

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

row = matrix[0]             # [1, 2, 3]
element = matrix[0][1]      # 2

print("matrix:", matrix)
print("first row:", row)
print("matrix[0][1]:", element)


# --- Positive Indexing ---

fruits = ['apple', 'banana', 'orange']
#          0        1         2

first = fruits[0]           # 'apple'
second = fruits[1]          # 'banana'
last = fruits[2]            # 'orange'

print("\nPositive indexing:")
print("first:", first)
print("second:", second)
print("last:", last)


# --- Negative Indexing ---

items = [10, 20, 30, 40, 50]
#        -5  -4  -3  -2  -1

last = items[-1]             # 50
second_last = items[-2]      # 40
first = items[-5]            # 10

print("\nNegative indexing:")
print("last (-1):", last)
print("second_last (-2):", second_last)
print("first (-5):", first)


# --- Nested List Indexing ---

matrix = [[1, 2, 3], [4, 5, 6]]

row = matrix[0]              # [1, 2, 3]
element = matrix[0][1]       # 2
last = matrix[-1][-1]        # 6

print("\nNested indexing:")
print("matrix[0]:", row)
print("matrix[0][1]:", element)
print("matrix[-1][-1]:", last)


# --- Finding Elements ---

items = ['a', 'b', 'c']

print("\nFinding elements:")
print("'b' in items:", 'b' in items)       # True
print("'d' in items:", 'd' in items)       # False
print("index of 'b':", items.index('b'))   # 1
print("length:", len(items))               # 3


# --- Safe Access ---

numbers = [1, 2, 3]
index = 10

if 0 <= index < len(numbers):
    value = numbers[index]
else:
    print(f"\nIndex {index} is out of bounds (list has {len(numbers)} items)")
