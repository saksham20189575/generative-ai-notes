# ============================================
# Iteration – Iterate Through Lists Using Loops
# ============================================


# --- Basic For Loop ---

fruits = ['apple', 'banana', 'orange']

print("Basic for loop:")
for fruit in fruits:
    print(f"  {fruit}")


# --- With Conditional ---

numbers = [1, 2, 3, 4, 5]

print("\nEven numbers:")
for num in numbers:
    if num % 2 == 0:
        print(f"  {num} is even")


# --- Accumulating a Result ---

numbers = [1, 2, 3, 4, 5]
total = 0

for num in numbers:
    total += num

print(f"\nSum of {numbers} = {total}")


# --- enumerate() — Index + Value ---

fruits = ['apple', 'banana', 'orange']

print("\nenumerate (start=0):")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

print("\nenumerate (start=1):")
for num, fruit in enumerate(fruits, start=1):
    print(f"  {num}. {fruit}")


# --- Modify Elements by Index ---

grades = [75, 82, 68]
print(f"\nGrades before: {grades}")

for i, grade in enumerate(grades):
    if grade < 80:
        grades[i] = 80

print(f"Grades after (min 80): {grades}")


# --- While Loop Iteration ---

print("\nWhile loop:")
fruits = ['apple', 'banana', 'orange']
i = 0

while i < len(fruits):
    print(f"  {fruits[i]}")
    i += 1


# --- Conditional Termination with While ---

numbers = [10, 20, 30, 40, 50]
i = 0

print("\nWhile with condition (stop at >= 40):")
while i < len(numbers) and numbers[i] < 40:
    print(f"  {numbers[i]}")
    i += 1


# --- zip() — Parallel Iteration ---

names = ['Alice', 'Bob', 'Charlie']
scores = [85, 92, 78]

print("\nzip - parallel iteration:")
for name, score in zip(names, scores):
    print(f"  {name}: {score}")


# --- zip with 3 lists ---

first = ['Alice', 'Bob']
last = ['Smith', 'Jones']
ages = [25, 30]

print("\nzip - three lists:")
for f, l, a in zip(first, last, ages):
    print(f"  {f} {l}, age {a}")


# --- Create Dictionary from zip ---

keys = ['name', 'age', 'city']
values = ['Alice', 25, 'NYC']

person = dict(zip(keys, values))
print(f"\nDict from zip: {person}")


# --- Safe Modification Patterns ---

# BAD: Don't modify while iterating
# numbers = [1, 2, 3, 4, 5]
# for num in numbers:
#     if num % 2 == 0:
#         numbers.remove(num)  # Can skip elements!

# GOOD: Iterate over a copy
numbers = [1, 2, 3, 4, 5]
for num in numbers[:]:
    if num % 2 == 0:
        numbers.remove(num)
print(f"\nRemove evens (copy method): {numbers}")

# BEST: List comprehension
numbers = [1, 2, 3, 4, 5]
numbers = [n for n in numbers if n % 2 != 0]
print(f"Remove evens (comprehension): {numbers}")

# SAFE: Modify values by index
numbers = [1, 2, 3, 4, 5]
for i in range(len(numbers)):
    numbers[i] *= 2
print(f"Double all (by index): {numbers}")


# --- Nested List Iteration ---

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

print("\nNested iteration (rows):")
for row in matrix:
    print(f"  {row}")

print("\nNested iteration (all elements):")
for row in matrix:
    for element in row:
        print(f"  {element}", end=" ")
    print()

print("\nNested with indices:")
for i, row in enumerate(matrix):
    for j, element in enumerate(row):
        print(f"  [{i}][{j}] = {element}")


# --- Loop Control: break, continue, else ---

print("\nbreak — exit early:")
for num in [1, 2, 3, 4, 5]:
    if num > 3:
        break
    print(f"  {num}")

print("\ncontinue — skip iteration:")
for num in [1, 2, 3, 4, 5]:
    if num % 2 == 0:
        continue
    print(f"  {num}")

print("\nfor-else — runs if no break:")
for num in [1, 2, 3]:
    if num > 10:
        break
else:
    print("  No large numbers found")
