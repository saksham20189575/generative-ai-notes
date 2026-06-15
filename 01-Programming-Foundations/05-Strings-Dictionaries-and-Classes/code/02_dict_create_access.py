# ============================================
# Dictionaries – Create, Initialize & Access
# ============================================


# --- What Is a Dictionary? ---

# Key-value pairs for structured data
student = {'name': 'Alice', 'age': 22, 'grade': 'A'}
print("student:", student)


# --- Why Dictionaries? (Before vs After) ---

# Positional (fragile — what's index 2?)
student_list = ['Alice', 22, 'A', 'alice@email.com']

# Dictionary (clear and self-documenting)
student_dict = {
    'name': 'Alice',
    'age': 22,
    'grade': 'A',
    'email': 'alice@email.com'
}
print("\nstudent['grade']:", student_dict['grade'])  # Crystal clear!


# --- Creating Dictionaries ---

# Literal syntax (most common)
person = {'name': 'Alice', 'age': 25}

# dict() constructor
person2 = dict(name='Alice', age=25)

# From list of tuples
person3 = dict([('name', 'Alice'), ('age', 25)])

# Empty dictionary
empty = {}

print("\nLiteral:", person)
print("dict():", person2)
print("From tuples:", person3)
print("Empty:", empty)


# --- Dictionary Comprehension ---

squares = {x: x**2 for x in range(1, 6)}
print("\nComprehension:", squares)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


# --- fromkeys() — Same Value for Multiple Keys ---

subjects = dict.fromkeys(['Math', 'Science', 'English'], 0)
print("fromkeys:", subjects)          # {'Math': 0, 'Science': 0, 'English': 0}


# --- Keys Must Be Unique ---

data = {'a': 1, 'b': 2, 'a': 3}
print("\nDuplicate key:", data)        # {'a': 3, 'b': 2} — last value wins


# --- Keys Must Be Immutable ---

d = {'name': 'Alice', 42: 'answer', (1, 2): 'tuple key'}
print("Various keys:", d)

# Lists cannot be keys (they're mutable):
# d = {[1, 2]: 'x'}  # TypeError: unhashable type: 'list'


# --- Nested Dictionaries ---

students = {
    'Alice': {'age': 22, 'grade': 'A'},
    'Bob': {'age': 24, 'grade': 'B'}
}

print("\nNested dict:", students)
print("Alice's grade:", students['Alice']['grade'])  # 'A'


# ============================================
# Accessing Values — [] vs .get()
# ============================================

student = {'name': 'Alice', 'age': 22}

# --- Square Brackets [] — Fail-Fast ---

print("\n--- Accessing with [] ---")
print("student['name']:", student['name'])  # Alice

# Missing key raises KeyError:
# print(student['email'])  # KeyError: 'email'


# --- .get() — Fail-Safe ---

print("\n--- Accessing with .get() ---")
print("get('name'):", student.get('name'))               # Alice
print("get('email'):", student.get('email'))              # None
print("get('email', 'not set'):", student.get('email', 'not set'))  # 'not set'


# --- When to Use Which ---

# [] — when key is guaranteed to exist (catches bugs)
# .get() — when key might not exist (graceful handling)


# --- keys(), values(), items() ---

student = {'name': 'Alice', 'age': 22, 'grade': 'A'}

print("\n--- keys, values, items ---")
print("keys():", list(student.keys()))       # ['name', 'age', 'grade']
print("values():", list(student.values()))   # ['Alice', 22, 'A']
print("items():", list(student.items()))     # [('name', 'Alice'), ...]


# --- Checking Key Existence with 'in' ---

print("\n--- 'in' keyword ---")
print("'name' in student:", 'name' in student)     # True
print("'email' in student:", 'email' in student)   # False

# 'in' checks KEYS, not values!
print("'Alice' in student:", 'Alice' in student)    # False (Alice is a value)

# Check values explicitly
print("'Alice' in values:", 'Alice' in student.values())  # True


# --- Safe Nested Access with .get() ---

data = {'user': {'name': 'Alice', 'address': {'city': 'Mumbai'}}}

city = data.get('user', {}).get('address', {}).get('city', 'Unknown')
print(f"\nNested get: {city}")  # Mumbai

missing = data.get('user', {}).get('phone', {}).get('number', 'N/A')
print(f"Missing nested: {missing}")  # N/A


# --- Practical: Word Frequency Counter ---

text = "the cat sat on the mat the cat"
words = text.split()
freq = {}

for word in words:
    freq[word] = freq.get(word, 0) + 1

print(f"\nWord frequency: {freq}")
# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}
