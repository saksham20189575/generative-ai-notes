# ============================================
# Dictionaries – Add, Modify & Remove Entries
# ============================================


# ============================================
# Adding & Modifying
# ============================================

# --- dict[key] = value (Upsert) ---

student = {'name': 'Alice', 'age': 22}
print("Original:", student)

# Add a new key
student['grade'] = 'A'
print("After add:", student)

# Modify an existing key
student['age'] = 23
print("After modify:", student)
# {'name': 'Alice', 'age': 23, 'grade': 'A'}


# --- update() — Multiple at Once ---

student = {'name': 'Alice', 'age': 22}
student.update({'age': 23, 'grade': 'A', 'city': 'Mumbai'})
print("\nAfter update():", student)

# update() with keyword arguments
config = {'theme': 'dark'}
config.update(font_size=14, language='en')
print("Config:", config)

# update() with list of tuples
data = {}
data.update([('name', 'Alice'), ('age', 25)])
print("From tuples:", data)


# --- setdefault() — Only If Missing ---

config = {'theme': 'dark'}

config.setdefault('language', 'en')    # Adds 'language' (missing)
config.setdefault('theme', 'light')    # Does NOT change 'theme' (exists)

print("\nAfter setdefault:", config)
# {'theme': 'dark', 'language': 'en'}


# --- |= Operator (Python 3.9+) ---

defaults = {'theme': 'light', 'lang': 'en'}
user_prefs = {'theme': 'dark'}
defaults |= user_prefs
print("\nAfter |=:", defaults)   # {'theme': 'dark', 'lang': 'en'}


# --- Counter Pattern ---

text = "hello world"
counts = {}
for char in text:
    if char != ' ':
        counts[char] = counts.get(char, 0) + 1

print("\nChar counts:", counts)


# --- Merge Without Modifying Originals ---

d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
merged = {**d1, **d2}       # d2 wins for key 'b'

print("\nd1:", d1)            # unchanged
print("d2:", d2)             # unchanged
print("merged:", merged)     # {'a': 1, 'b': 3, 'c': 4}


# --- Summary Table ---
# | Method               | Adds? | Overwrites? | Multiple? |
# |----------------------|-------|-------------|-----------|
# | d[key] = val         | Yes   | Yes         | No        |
# | d.update(...)        | Yes   | Yes         | Yes       |
# | d.setdefault(k, v)   | Yes   | No          | No        |
# | d |= other           | Yes   | Yes         | Yes       |


# ============================================
# Removing Entries
# ============================================

print("\n" + "=" * 40)
print("REMOVING ENTRIES")
print("=" * 40)

# --- del — Remove by Key ---

student = {'name': 'Alice', 'age': 22, 'grade': 'A'}
del student['grade']
print("\nAfter del:", student)    # {'name': 'Alice', 'age': 22}

# del with missing key raises KeyError:
# del student['email']  # KeyError


# --- pop() — Remove and Return Value ---

student = {'name': 'Alice', 'age': 22, 'grade': 'A'}
age = student.pop('age')
print(f"\nPopped 'age': {age}")
print("After pop:", student)

# pop() with default (safe — no KeyError)
missing = student.pop('email', 'not found')
print(f"Pop missing key: {missing}")


# --- popitem() — Remove Last Inserted Pair ---

student = {'name': 'Alice', 'age': 22, 'grade': 'A'}
last_pair = student.popitem()
print(f"\npopitem(): {last_pair}")      # ('grade', 'A')
print("After popitem:", student)


# --- clear() — Empty the Dictionary ---

student = {'name': 'Alice', 'age': 22}
student.clear()
print(f"\nAfter clear(): {student}")     # {}


# --- Safe Deletion of Multiple Keys ---

data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
keys_to_remove = ['b', 'd', 'z']        # 'z' doesn't exist

for key in keys_to_remove:
    data.pop(key, None)                  # None = no error if missing

print(f"\nAfter safe removal: {data}")   # {'a': 1, 'c': 3}


# --- Never Modify Dict While Iterating ---

# BAD:
# for key in data:
#     if some_condition:
#         del data[key]  # RuntimeError!

# GOOD: Collect keys first, then delete
data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
keys_to_delete = [k for k, v in data.items() if v % 2 == 0]

for key in keys_to_delete:
    del data[key]

print(f"After filtered delete: {data}")  # {'a': 1, 'c': 3}


# --- Comparison Table ---
# | Method          | Returns Value? | Error if Missing?     |
# |-----------------|---------------|----------------------|
# | del d[key]      | No            | Yes (KeyError)       |
# | d.pop(key)      | Yes           | Yes (unless default) |
# | d.pop(key, def) | Yes/default   | No                   |
# | d.popitem()     | Yes (pair)    | Yes (if empty)       |
# | d.clear()       | No            | No                   |
