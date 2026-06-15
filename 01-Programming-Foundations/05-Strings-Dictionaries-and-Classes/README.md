## Implement String Data Types

---

<div align="center">

![Python String Character Indexing](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.5.png)

*Strings are immutable sequences of characters — Python provides rich methods for slicing, searching, and transforming text*

</div>

---

## Understanding Strings

### Why "String"?
"String" means "string of characters" — like beads on a string. It's a **sequence** of characters:
"Hello" = ['H', 'e', 'l', 'l', 'o']

### From Numbers to Text
Each character is assigned a number (character encoding):
- **ASCII** (1960s): 128 characters (English, digits, symbols)
- **Unicode** (1991): 1 million+ characters (all languages, emoji) 😊
Python 3 uses Unicode by default, e.g., `message = "Hello 世界 🌍"`.

### Strings Are Immutable
Once created, strings cannot be changed. Any "modification" creates a **new** string:
```python
name = "Alice"
name = name.upper()  # Creates new string "ALICE"
```
**Why immutable?** Safety, efficiency, and allows use as dictionary keys.

## Creating Strings

### Using Quotes
```python
name = 'Alice'
message = "He said, 'Hello!'"  # mix quotes, or escape \" inside the same quote style
```

### Multi-line Strings
```python
long_text = """This is a
multi-line string."""
```

---

## String Operations

### Concatenation (+) and Repetition (*)
```python
result = "Hello" + " " + "World"
message = "Age: " + str(25)
line = "=" * 20
```

### Length
```python
name = "Alice"
length = len(name) # 5
```

---

## String Methods

### Common methods
```python
name = "  alice  "
print(name.strip().title())           # "Alice"
print("Hello World".replace("World", "Python"))
email = "user@example.com"
print(email.startswith("user"), "@" in email)  # True True
```

---

## Practical Example

```python
first_name = "Alice"
last_name = "Johnson"
full_name = first_name + " " + last_name  # "Alice Johnson"
```

---

## Key Takeaways
1. Strings are text in quotes.
2. Use `+` to concatenate, `*` to repeat.
3. Convert numbers to strings (`str()`) before concatenating.
4. Many useful string methods (e.g., `upper()`, `lower()`, `strip()`, `replace()`).
5. Use `len()` to get length.

---

## Creating and Initializing Dictionaries for Key-Value Pairs

---

## Introduction

Dictionaries are Python's implementation of **hash maps** (or associative arrays) — a fundamental data structure for organizing data by **meaning** (keys) instead of position. They provide **O(1)** (constant time) average lookup speed.

---

<div align="center">

![Python Dictionary Key-Value Pairs](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.18.png)

*Dictionaries are hash tables — keys are hashed to array indices for O(1) access to their associated values*

</div>

---

### Why Dictionaries Are Revolutionary

**Before dictionaries** (positional thinking):
```python
student = ['Alice', 22, 'A', 'alice@email.com']
# What's index 2? Grade or email? Fragile and error-prone!
```

**With dictionaries** (semantic thinking):
```python
student = {'name': 'Alice', 'age': 22, 'grade': 'A', 'email': 'alice@email.com'}
print(student['grade'])  # Crystal clear! Add/reorder fields without breaking code.
```

**Historical Context**: Concept from SNOBOL (1962), AWK (1977). Python's `dict` (1991) implemented as hash table. Guido van Rossum chose "dictionary" for its intuitive lookup analogy. Python 3.7+ guarantees insertion order.

**Real-World Analogy**: Like a **phonebook** where a person's name (key) instantly gives you their number (value). No need to scan page by page. This O(1) access is how databases and caches work internally.

**Hash Table Foundation**: Keys are **hashed** to an internal array index, allowing direct, constant-time retrieval of values. This is why keys must be immutable (hashable); a mutable key's hash could change, making the value unretrievable.

**Self-Documenting Power**: Dictionaries make code inherently clearer — e.g. `{'debug': True, 'port': 5432}` states intent without extra comments.

---

### What Is a Dictionary?

A **dictionary** stores data as **key-value pairs**.

```python
student = {'name': 'Alice', 'age': 22, 'grade': 'A'}
```

**Key Properties:**
1.  **Key-value pairs** — every entry has a key and a value.
2.  **Keys must be unique** — duplicate keys overwrite previous values.
3.  **Keys must be immutable** — strings, numbers, tuples are valid.
4.  **Values can be anything** — strings, lists, other dicts, etc.
5.  **Ordered** (Python 3.7+) — insertion order is preserved.

---

### Creating Dictionaries

```python
person = {'name': 'Alice', 'age': 25}
person = dict(name='Alice', age=25)  # or dict([('name', 'Alice'), ('age', 25)])
empty = {}
```

---

### Dictionary Comprehension

Create dictionaries with a compact expression:
```python
squares = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

---

### `dict.fromkeys()` — Same Value for Multiple Keys

```python
subjects = dict.fromkeys(['Math', 'Science', 'English'], 0)
# {'Math': 0, 'Science': 0, 'English': 0}
```

---

### Keys Must Be Unique

Using the same key twice overwrites the previous value:
```python
data = {'a': 1, 'b': 2, 'a': 3}
print(data)  # {'a': 3, 'b': 2}
```

---

### What Can Be Keys?

Keys must be **immutable** (e.g. str, int, tuple). Lists and dicts cannot be keys.
```python
d = {'name': 'Alice', 42: 'answer'}
# d = {[1, 2]: 'x'}  # TypeError
```

---

### Nested Dictionaries

Dictionaries can store other dictionaries as values, forming hierarchical structures.

```python
students = {
    'Alice': {'age': 22, 'grade': 'A'},
    'Bob': {'age': 24, 'grade': 'B'}
}

print(students['Alice']['grade'])      # 'A'
```

---

### Practical Example

```python
text = "the cat sat on the mat the cat"
words = text.split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq)  # {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}
```

---

### Quick Reference

| Method | Example | Result |
|--------|---------|--------|
| Literal | `{'a': 1, 'b': 2}` | Dict with 2 pairs |
| `dict()` | `dict(a=1, b=2)` | Same as above |
| From tuples | `dict([('a',1), ('b',2)])` | Same as above |
| Comprehension | `{x: x**2 for x in range(3)}` | `{0:0, 1:1, 2:4}` |
| `fromkeys()` | `dict.fromkeys(['a','b'], 0)` | `{'a':0, 'b':0}` |
| Empty | `{}` or `dict()` | Empty dict |

---

### Key Takeaways

1.  Dictionaries store **key-value pairs** for structured data.
2.  Multiple creation methods: `{}`, `dict()`, comprehensions, `fromkeys()`.
3.  Keys must be **unique** and **immutable**.
4.  Values can be **any type**.
5.  Order is **preserved** (Python 3.7+).
6.  Perfect for **structured data**, **lookups**, and **configurations**.

---

## Accessing Dictionary Values Using Keys and get() Method

---

## Introduction

`[]` vs `.get()` is about **fail-fast vs. fail-safe** error handling.

---

<div align="center">

![Python Dictionary get() Method Access](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.19.png)

*dict[key] and dict.get(key) both look up values by hashing the key — the difference is how they handle missing keys*

</div>

---

### Why Two Access Methods? Design Philosophy

**`dict[key]` = Fail-Fast:**
- Key **MUST** exist! Missing key → `KeyError`.
- Use during **development** to catch bugs immediately.

**`dict.get(key, default)` = Fail-Safe:**
- Key **might not** exist. Missing key → returns `default` value.
- Use in **production** for graceful degradation.

**Analogy**: `[]` is a **strict vending machine** (crashes if item missing). `.get()` is a **friendly assistant** (offers default if item missing).

### The Graceful Degradation Pattern

```python
config = {'theme': 'dark'}
font_size = config.get('font_size', 14)  # missing key → 14, no KeyError
```

**Word counting:** `counts[w] = counts.get(w, 0) + 1`.

---

### Accessing with Square Brackets `[]`

```python
student = {'name': 'Alice'}
print(student['name'])   # Alice — KeyError if key missing
```

---

### Accessing with `.get()` — Safe Access

```python
student = {'name': 'Alice'}
print(student.get('email', 'not set'))  # 'not set'
```

`get(key, default)` returns the value if key exists, `default` (or `None`) if not.

---

### When to Use `[]` vs `.get()`

| Situation | Use | Why |
|-----------|-----|-----|
| Key is guaranteed to exist | `dict[key]` | Clear, direct |
| Key might not exist | `dict.get(key, default)` | Avoids KeyError, handles defaults |

---

### Accessing All Keys, Values, and Items

```python
student = {'name': 'Alice', 'age': 22}
print(student.keys())    # dict_keys(['name', 'age'])
print(student.values())  # dict_values(['Alice', 22])
print(student.items())   # dict_items([('name', 'Alice'), ('age', 22)])
```

Convert to lists: `list(student.keys())`

---

### Checking if a Key Exists

`in` checks **keys**, not values (`'Alice' in student` is `False` for the dict above).
```python
student = {'name': 'Alice'}
if 'email' not in student:
    student['email'] = 'unknown@example.com'
```

---

### Accessing Nested Dictionaries

```python
data = {'user': {'name': 'Alice', 'address': {'city': 'Mumbai'}}}
city = data.get('user', {}).get('address', {}).get('city', 'Unknown')
```

---

### Practical Example

```python
profile = {'name': 'Alice', 'theme': 'dark'}
print(f"{profile.get('name', 'Guest')} — lang {profile.get('language', 'en')}")
```

---

### Key Takeaways

1.  `dict[key]` — direct access, raises `KeyError` if key missing
2.  `dict.get(key)` — safe access, returns `None` if key missing
3.  `dict.get(key, default)` — safe access with custom fallback
4.  Use `in` to check if a **key** exists
5.  `.keys()`, `.values()`, `.items()` give views of dictionary contents
6.  Chain `.get()` for safe nested dictionary access

---

## Adding and Modifying Dictionary Entries

Dictionary modification showcases **mutable mapping** design: `dict[key] = value` performs an **upsert** (update if key exists, insert if new), making it context-sensitive.

<div align="center">

![Python Dictionary Add Update Key Value Pair](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.20.png)

*`dict[key] = value` performs an upsert: if the key exists, its value is updated; if not, a new entry is inserted*

</div>

### Why Unified Add/Modify Syntax is Elegant
Python's `student['age'] = 23` is simple, clean, and requires no `if`-check. This is **"upsert"** (UPDATE or INSERT) behavior, common in databases.

### Real-World Analogy
**Dict modification is like updating contacts**: Your phone doesn't ask "add or update?" – it just saves the number under a name, adding if new, replacing if existing. Python dicts work the same way.

### The `setdefault()` Design Genius
**Problem**: Initialize a key if missing, otherwise keep its current value.
**Verbose approach**: `if 'count' not in data: data['count'] = 0`.
**Elegant solution**: `data.setdefault('count', 0)`.
**Why brilliant**: It combines **check + set + get** in one atomic, efficient operation. Crucial for grouping and accumulation patterns.

### Adding & Modifying Entries
Use `dict[key] = value`.
- **Adding**: Assign to a new key.
- **Modifying**: Assign to an existing key, overwriting its value.
```python
student = {'name': 'Alice', 'age': 22}
student['grade'] = 'A'  # Add new
student['age'] = 23      # Modify existing
print(student) # {'name': 'Alice', 'age': 23, 'grade': 'A'}
```

### The `update()` Method
Add or modify **multiple** entries at once. Existing keys are overwritten; new keys are added.
```python
student = {'name': 'Alice', 'age': 22}
student.update({'age': 23, 'grade': 'A', 'city': 'Mumbai'})
print(student) # {'name': 'Alice', 'age': 23, 'grade': 'A', 'city': 'Mumbai'}
```

### The `setdefault()` Method
Sets a value **only if the key doesn't already exist** (also returns the value).
```python
config = {'theme': 'dark'}
config.setdefault('language', 'en')  # adds 'language'; 'theme' unchanged
```

### The `|=` Operator (Python 3.9+)
Merge another dictionary into the current one, modifying in place. Values from the right-hand dictionary override those from the left.
```python
defaults = {'theme': 'light', 'lang': 'en'}
user_prefs = {'theme': 'dark'}
defaults |= user_prefs
print(defaults)  # {'theme': 'dark', 'lang': 'en'}
```

### Incrementing Values (Counter Pattern)
Same idea as word counts: `counts[k] = counts.get(k, 0) + 1`.

### Practical Example

```python
default_config = {'debug': False, 'port': 3000}
env_config = {'debug': True, 'port': 8080}
final = {**default_config, **env_config}
```

### Summary Table
| Method | Adds New? | Overwrites? | Multiple? |
|--------|-----------|-------------|-----------|
| `d[key] = val` | Yes | Yes | No |
| `d.update(...)` | Yes | Yes | Yes |
| `d.setdefault(key, val)` | Yes | **No** | No |
| `d \|= other` | Yes | Yes | Yes |

### Key Takeaways
1.  `dict[key] = value` — adds or overwrites a single entry.
2.  `dict.update()` — adds/overwrites multiple entries at once.
3.  `dict.setdefault()` — only sets if key is missing (safe initialization).
4.  Use `.get()` with increment for counting patterns.
5.  Use `{**d1, **d2}` or `|=` for merging dictionaries.

---

## Removing Entries Using pop(), popitem(), and del

<div align="center">

![Python Dictionary pop() Remove Entry](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.21.png)

*del removes by key, pop() removes and returns the value, popitem() removes the last inserted pair (LIFO)*

</div>

### Why Multiple Removal Methods?
*   `del` (statement): Low-level, permanent removal by key.
*   `pop()`: Removes and **returns** the value (retrieval + removal).
*   `popitem()`: Removes and returns the **last** inserted key-value pair (LIFO stack behavior).
*   `clear()`: Removes **all** entries, emptying the dictionary.
Each method serves a distinct purpose for different use cases.

### `del`, `pop`, `popitem`, and `clear`
`del d[k]` drops a pair (raises `KeyError` if missing). `d.pop(k)` removes and returns the value; use `d.pop(k, default)` to avoid errors. `d.popitem()` removes the **last inserted** pair. `d.clear()` empties the dict.
```python
student = {'name': 'Alice', 'age': 22, 'grade': 'A'}
del student['grade']
student.pop('age')
student.popitem()          # removes last pair (here: 'name')
student.clear()

data = {'a': 1, 'b': 2, 'c': 3}
for key in ['b', 'd']:
    data.pop(key, None)    # 'd' ignored — no KeyError
```

### Comparison Table
| Method | Returns Value? | Key Required? | Error if Missing? |
|--------|---------------|---------------|-------------------|
| `del d[key]` | No | Yes | Yes (KeyError) |
| `d.pop(key)` | Yes | Yes | Yes (unless default given) |
| `d.pop(key, default)` | Yes (or default) | Yes | No |
| `d.popitem()` | Yes (last pair) | No | Yes (if empty) |
| `d.clear()` | No | No | No |

### Safe Deletion Patterns
Remove several keys safely with `pop(key, None)` (shown below). **Do not** change a dict while iterating its keys — collect keys to remove first, then delete.

### Key Takeaways
1.  `del d[key]` — simple, no return, errors on missing key.
2.  `pop(key)` — removes, returns value, can use default.
3.  `popitem()` — removes last pair (LIFO).
4.  `clear()` — empties the dictionary.
5.  Use `pop(key, None)` for safe removal without explicit `if` check.
6.  Never modify dict while iterating directly; collect keys first.

---

## Checking for Key Existence Using the 'in' Keyword

## Introduction
The `in` operator provides **O(1) membership testing** for dictionary keys, enabling **defensive programming** to prevent `KeyError` crashes. This is a "look before you leap" (LBYL) approach.

<div align="center">

![Python Dictionary Key Existence Check](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.22.jpg)

*The `in` keyword uses hash lookup — O(1) for dicts/sets vs O(n) for lists, making it ideal for membership checks*

</div>

### The `in` Operator for Dictionaries
`in` checks **keys**, not values (`'Alice' in student` is `False` if `'Alice'` is only a value).
```python
student = {'name': 'Alice', 'age': 22}
print('name' in student, 'email' in student)  # True False
```

### Why Check for Keys?
Use `'key' in d` before `d['key']`, or use `d.get('key', default)` to avoid `KeyError`.

### `in` vs `.get()` vs `try/except`
Use **`in`** when branches depend on existence; **`.get(key, default)`** for a simple fallback; **`try`/`except KeyError`** when missing keys are unusual (EAFP). For nested dicts, chain `.get(..., {})` as in **Accessing Nested Dictionaries** (earlier in these notes).

### Checking Values (Not Keys)
Use `value in dict.values()` when you care about values, not keys.

### Common Patterns
```python
config = {'port': 8080}
if 'host' not in config:
    config['host'] = 'localhost'
```

### Performance
Key lookup with `in` is **O(1)** on average due to dictionaries using hash tables internally.

### Key Takeaways
1. `key in dict` checks if a **key** exists — O(1) operation.
2. `in` does NOT check values — use `val in dict.values()` for that.
3. Use `in` when you need conditional logic based on key existence.
4. Use `.get()` when you just need a fallback value.
5. Always check before `del` or `[]` access to avoid `KeyError`.

---

## Iterating Through Dictionary Keys, Values, and Items

### Introduction
Dictionary iteration provides **three view objects**: `keys`, `values`, or `items` (key-value pairs). These are **live views** into the dictionary, not copies, and update automatically with dictionary changes.

<div align="center">

![Python Dictionary keys() values() items() Iteration](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.23.png)

*.keys() iterates over keys, .values() over values, .items() over (key, value) tuples — three views of the same data*

</div>

### Why Three Iteration Methods?
*   **Keys only** (`.keys()` or default): For identifiers.
*   **Values only** (`.values()`): For aggregating/analyzing data.
*   **Key-value pairs** (`.items()`): For context with each value.

### Dictionary Views Are Live!
`keys()`, `values()`, and `items()` return **views** that reflect the dict if it changes later.

### Three Ways to Iterate
`for key in d` is the same as `for key in d.keys()`. Use `sorted(d)` or `sorted(d, key=d.get)` when order matters.
```python
student = {'name': 'Alice', 'age': 22}
for key, value in student.items():
    print(f"{key}: {value}")
prices = {'apple': 1.50, 'banana': 0.75}
total = sum(prices.values())
```

### Comprehensions and `max` / `min` with dicts
```python
scores = {'Alice': 92, 'Bob': 45}
passing = {name: s for name, s in scores.items() if s >= 50}
top_student = max(scores, key=scores.get)
```

### Key Takeaways
1. `for key in dict` — iterates over keys; `values()` / `items()` for those views.
2. Dict comprehensions and `max(d, key=d.get)` are common patterns.
3. Use `sorted(d)` or `sorted(d, key=d.get)` when order matters.
4. Never modify a dict while iterating over it — build a new one first.

---

## Merging Dictionaries Using the update() Method

## Introduction
Dictionary merging, a fundamental software engineering pattern, enables **configuration layering**. This allows settings from sources like defaults, config files, environment variables, and command-line arguments to override each other, establishing precedence. This is how modern applications handle configuration.

<div align="center">

![Python Merge Dictionaries update() Method](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.2/LO-9.2.24.png)

*update() merges two dictionaries — existing keys get overwritten by the new values, new keys are added*

</div>

### Why Merging is Fundamental
Apps merge settings from many sources; **later** dicts override earlier ones for the same key (e.g. `{**defaults, **overrides}`).

### The Evolution of Dict Merging
**Python 3.5**: Introduced `{**d1, **d2}` unpacking for clean merging.
**Python 3.9**: Added the `|` operator, offering even cleaner syntax, inspired by set union.

### The `update()` Method
Merges another dictionary (or key-value pairs) into the current dictionary, modifying it in place.

```python
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
d1.update(d2)
print(d1) # {'a': 1, 'b': 3, 'c': 4}
```
**Behavior:**
- New keys are **added**.
- Existing keys are **overwritten** (last value wins).
- `d1` is modified in place; `d2` is unchanged.

### Different Ways to Call `update()`
1.  **With another dictionary:** `base.update({'port': 8080})`
2.  **With keyword arguments:** `config.update(font_size=14)`
3.  **With a list of tuples:** `data.update([('name', 'Alice')])`

### Merging Without Modifying Originals
**Unpacking:** `merged = {**defaults, **user_prefs}` — originals unchanged.
**Python 3.9+:** `merged = defaults | user_prefs` (new dict) or `defaults |= user_prefs` (in place).

### Merge Priority
Right-hand / later mappings win for duplicate keys: `{**d1, **d2}` → `d2`'s values override `d1`'s.

### Practical Example
```python
default_config = {'debug': False, 'port': 3000}
env_config = {'port': 8080}
cli_config = {'debug': True}
final_config = {**default_config, **env_config, **cli_config}
```

### Comparison Table
| Method | Modifies Original? | Python Version |
|--------|-------------------|----------------|
| `d1.update(d2)` | Yes | All |
| `{**d1, **d2}` | No (new dict) | 3.5+ |
| `d1 \| d2` | No (new dict) | 3.9+ |
| `d1 \|= d2` | Yes | 3.9+ |

### Key Takeaways
1.  `update()` merges a dict in place; later values overwrite earlier ones.
2.  `{**d1, **d2}` and `|` create new merged dicts, preserving originals.
3.  Order dictates priority: the last dict in sequence wins for shared keys.
4.  Merging is **shallow**: nested dicts are replaced entirely.
5.  For custom merge logic (e.g., combining lists, summing values), a dedicated function is required.

---

## List Essentials (Built-ins and Common Methods)

Lists are **mutable sequences**. These show up constantly alongside strings and dictionaries.

### Built-in functions (take any iterable; lists are typical)

| Function | Typical use |
|----------|-------------|
| `len(lst)` | Number of items |
| `sum(lst)` | Sum of numbers |
| `max(lst)` / `min(lst)` | Largest / smallest item |
| `sorted(lst)` | **New** sorted list; leaves `lst` unchanged |
| `reversed(lst)` | Iterator over items in reverse (`list(...)` if you need a list) |
| `enumerate(lst)` | `(index, value)` in `for` loops |
| `zip(a, b)` | Walk two (or more) lists in parallel |

```python
nums = [3, 1, 4]
print(len(nums), sum(nums), sorted(nums))  # 3 8 [1, 3, 4]
for i, x in enumerate(nums):
    print(i, x)
```

### Common list **methods** (mutate the list in place unless noted)

| Method | Role |
|--------|------|
| `append(x)` | Add one element at the end |
| `extend(iter)` | Append all items from another iterable |
| `insert(i, x)` | Insert at index |
| `pop()` / `pop(i)` | Remove and return last item or item at `i` |
| `remove(x)` | Remove first occurrence of `x` |
| `sort()` | Sort in place (`None` return); contrasts with built-in `sorted()` |
| `reverse()` | Reverse in place |
| `count(x)` | Number of times `x` appears |
| `index(x)` | Index of first `x` (raises `ValueError` if missing) |

```python
items = [2, 3, 2]
items.append(5)
items.sort()
```

**Remember:** `sorted(x)` returns a new list; `x.sort()` sorts `x` and returns `None`.

---

# Define Classes

## Classes in Python
A class is a blueprint for creating objects, defining their structure and behavior.

<div align="center">

![Python Class Blueprint OOP Concept](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.3/LO-9.3.19.png)

*Classes serve as blueprints in Python's type hierarchy, defining the structure for creating objects*

</div>

## Introduction
Classes implement **object-oriented programming (OOP)**: data and behavior live together in objects (**encapsulation**). A class is a **blueprint**; each object is one concrete instance.

### Historical Context
OOP invented by **Simula 67** (1967). **Smalltalk** (1972) popularized "everything is an object".

### Real-World Analogy
**Classes are like cookie cutters**:
- **Class**: Cookie cutter shape (blueprint)
- **Objects**: Actual cookies (instances)
One blueprint, many instances!

---
### Basic Syntax and naming
```python
class ClassName:
    pass
```
Use **PascalCase** (e.g. `BankAccount`).

## Classes and methods
```python
class Dog:
    def bark(self):
        print("Woof!")

my_dog = Dog()
my_dog.bark()
```

## Key Takeaways
1. **`class` keyword**: Defines classes.
2. **PascalCase**: Naming convention.
3. **Blueprint**: Class is template, object is instance.
4. **Methods**: Functions inside classes.
5. **`self`**: First parameter of methods.

---

# Create Objects

## Creating Objects (Instances)
An object is a specific instance of a class. You create multiple objects from a single class definition.

<div align="center">
![Python Class Instantiation Object Creation](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.3/LO-9.3.20.png)
</div>

*Creating objects from classes works like a function machine: input parameters, output a new object*

## What is Instantiation?
**Instantiation** is the process of creating a concrete instance (object) from an abstract class blueprint. This defines the **class-instance relationship**.

### Why Instances Matter
Each object (instance) created from a class has:
-   **Unique identity**: A different memory address.
-   **Own state**: Independent data and attribute values.
-   **Shared behavior**: Methods defined by the class.
This ensures **instance independence**.

### Origin & Memory
**Simula 67** (1967) introduced object creation. Python uses `ClassName()` syntax (like a function call). Object creation allocates memory on the **heap**. Python's **garbage collector** automatically reclaims memory from unused objects (using reference counting and cycle detection).

### Analogy: Baking Cookies
-   **Class Cookie**: The recipe or cookie cutter (blueprint).
-   **cookie1, cookie2**: The actual cookies you bake (instances).
-   All follow the same recipe but are unique, individual cookies.

## Syntax
```python
object_name = ClassName(arguments_if_any)
```

## Basic instantiation
Each `ClassName()` call builds a **new** object (its own identity in memory).
```python
class Dog:
    pass

dog1 = Dog()
dog2 = Dog()
# dog1 and dog2 are different objects
```

## Objects are independent
```python
class Student:
    def __init__(self, name):
        self.name = name

alice = Student("Alice")
bob = Student("Bob")
alice.name = "Alicia"
print(alice.name, bob.name)  # Alicia Bob
```

## Real-World Example: Bank Accounts
```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposited ${amount}. New balance: ${self.balance}")
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{self.owner} withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Insufficient funds!")

alice_account = BankAccount("Alice", 1000)
bob_account = BankAccount("Bob", 500)

alice_account.deposit(200)
bob_account.withdraw(100)
```

## Storing Objects in Collections
```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

products = [
    Product("Laptop", 999),
    Product("Mouse", 25),
]

total_value = 0
for product in products:
    total_value += product.price
print(f"Total inventory value: ${total_value}")
```

## Key Takeaways
1.  **Multiple objects**: Create many instances from one class definition.
2.  **Independent**: Each object has its own unique data/state.
3.  **Same interface**: All objects from the same class share the same methods.
4.  **Memory**: Each object is stored in a separate memory location.
5.  **Collections**: Objects can be stored and managed within lists, dictionaries, etc.

---

# Implement the __init__ Constructor

## The __init__ Method
`__init__` is a special method (constructor) that automatically runs when you create an object.

<div align="center">

![Python __init__ Constructor Method Object](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.3/LO-9.3.21.png)

*The __init__ constructor acts as a function machine, transforming input parameters into initialized object state*

</div>

## Introduction
`__init__` provides constructor functionality, ensuring automatic initialization when objects are created. It's the "object birth certificate", setting initial state before the object enters the world. This is fundamental to RAII (Resource Acquisition Is Initialization) and guaranteed initialization!

### Why __init__ is Revolutionary
Without initialization, attributes may be missing (`AttributeError`). With `__init__`, you set required state as soon as the object is created — e.g. `Dog("Buddy")` always has `name`.

### Historical Context
Constructors were invented by **Simula 67** (1967). Python's `__init__` is technically an **initializer** (not a constructor) — `__new__` creates the object, `__init__` initializes it. This two-phase construction is invoked automatically when you create an object.

### Real-World Analogies
`__init__` is like a **birth certificate**: An object is created (`__new__`), then `__init__` records its initial data (name, etc.), giving it a complete identity.

### Constructor vs Regular Method
**Regular methods**: Called manually, e.g., `obj.setup()`. This can be forgotten.
**Constructor (`__init__`)**: Called automatically when the object is created, e.g., `obj = MyClass()`. This guarantees initialization.

### Syntax
```python
class ClassName:
    def __init__(self, parameters):
        # Initialize attributes
        self.attribute = value
```

## Why Use __init__?
1.  **Initialize attributes**: Set starting values for an object.
2.  **Automatic execution**: Runs when object is created.
3.  **Required data**: Ensure objects start with necessary data.

## Without __init__ vs With __init__
```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

dog = Dog("Buddy", "Labrador")  # attributes ready immediately
```

## The self Parameter
`self` refers to the object being created:
```python
class Car:
    def __init__(self, brand, year):
        self.brand = brand  # THIS object's brand
        self.year = year    # THIS object's year

car1 = Car("Toyota", 2020)
car2 = Car("Honda", 2021)
print(car1.brand)  # Toyota (car1's brand)
print(car2.brand)  # Honda (car2's brand)
```

## Validation and derived fields in __init__
You can check inputs or set computed attributes when the object is built:
```python
class Person:
    def __init__(self, name, age):
        self.name = name or "Unknown"
        self.age = max(0, age)

class Employee:
    def __init__(self, name, hourly_rate, hours_worked):
        self.name = name
        self.salary = hourly_rate * hours_worked
```

## __init__ with No Parameters
```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

counter = Counter()
counter.increment()
print(counter.count)  # 1
```

## Common Mistakes
- Assign with **`self.name = name`**, not `name = name`.
- Always define **`def __init__(self, ...)`** — include `self` as the first parameter.
- Indent the **body of the class** and **`__init__`** one level inside `class`.

## Key Takeaways
1.  **`__init__`**: Constructor method, runs automatically.
2.  **`self`**: First parameter, refers to the object.
3.  **Initialize attributes**: Set starting values.
4.  **Automatic**: Called when creating object.
5.  **Required data**: Use parameters to require necessary data.
6.  **Default values**: Can provide default parameter values.
7.  **Validation**: Can validate data in `__init__`.