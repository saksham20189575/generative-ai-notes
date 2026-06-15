## Operators & Conditional Statements
### Apply Logical Operators

## Introduction

Logical operators combine boolean conditions: **`and`**, **`or`**, and **`not`**. They implement **Boolean algebra** (digital logic, SQL `WHERE`, search operators, and every language’s conditionals). In code they are the building blocks of complex decisions.

---

<div align="center">

![Python Logical Operators Truth Table](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.14.png)

*Truth tables for AND, OR, and NOT — Python’s `and`, `or`, and `not` follow these rules*

</div>

---

**Analogies:** **AND** = all requirements (license *and* age *and* vehicle). **OR** = any option works (cash *or* card). **NOT** = opposite (`not raining`). Stacked filters: all must apply (**AND**); either source is fine (**OR**).

## The three operators

| Operator | Meaning | `True` when |
|----------|---------|-------------|
| `and` | Both must hold | Both are `True` |
| `or` | At least one holds | One or both `True` |
| `not` | Negation | Operand is `False` |

### `and` — truth table

| A | B | A and B |
|---|---|---------|
| True | True | **True** |
| True | False | False |
| False | True | False |
| False | False | False |

```python
age, has_license = 20, True
can_drive = age >= 18 and has_license  # True

score, submitted = 85, False
can_pass_course = score >= 60 and submitted  # False — one False ⇒ False

qualifies = age >= 21 and 50000 >= 30000 and True  # loan-style check
```

### `or` — truth table

| A | B | A or B |
|---|---|--------|
| True | True | **True** |
| True | False | **True** |
| False | True | **True** |
| False | False | False |

```python
can_sleep_in = True or False  # True if weekend OR holiday
is_bad_weather = False or False  # False only if both false

has_access = False or True  # admin OR owner
```

### `not` — truth table

| A | not A |
|---|-------|
| True | False |
| False | True |

```python
is_sunny = not False
is_adult = not (16 < 18)  # same idea as age >= 18
can_edit = not False  # e.g. form not yet submitted
```

## Combining operators

```python
age = 17
has_parent_consent, has_id = True, True
# Register if adult OR (minor with consent and id)
can_register = (age >= 18) or (age < 18 and has_parent_consent and has_id)
```

## Operator precedence

Order: **parentheses** → **`not`** → **`and`** → **`or`**.

```python
True or True and False   # True or (True and False) ⇒ True
(True or True) and False # False — parentheses change meaning

age, has_license = 17, False
has_permit, has_supervisor = True, True
can_proceed = (age >= 18 and has_license) or (has_permit and has_supervisor)
```

## Short-circuit evaluation

Evaluation is left-to-right; stops when the result is fixed. **`and`**: if the first part is falsy, the rest is skipped. **`or`**: if the first part is truthy, the rest is skipped.

```python
def expensive_check():
    print("called")
    return True

16 >= 18 and expensive_check()  # expensive_check never runs
True or expensive_check()        # never runs

username = None
is_valid = username is not None and len(username) > 0  # safe: no len(None)
```

## Common patterns

```python
# Range (Python chaining)
age = 30
18 <= age <= 65  # working-age style check

# Many requirements
username, password = "john_doe", "secret123"
is_valid = len(username) >= 3 and len(password) >= 8 and username != password

# Default with or (falsy left → right side)
display_name = "" or "Guest"   # "Guest"
display_name = "Alice" or "Guest"  # "Alice"
```

## Common mistakes

```python
# Use and/or for booleans, not &/| (bitwise)
True and False  # correct for logic

# Parentheses avoid surprises
age, has_license = 20, True
# Unclear:
# age >= 18 and has_license or not has_license
# Clearer when you mean something specific:
can_drive = (age >= 18 and has_license)

# Redundant
is_adult = (age >= 18) == True  # worse
is_adult = age >= 18           # better
```

## Practice exercise

Predict the output, then run mentally or in Python:

```python
a, b, c = True, False, True
print(a and b)
print(a or b)
print(not b)
print(a and b or c)
print(a and (b or c))
print(not (a and b))
```

<details>
<summary>Answers</summary>

`False`, `True`, `True`, `True`, `True`, `True` — note `a and b or c` is `(a and b) or c` by precedence.

</details>

## Key takeaways

1. **`and`**: both must be `True`.
2. **`or`**: at least one `True`.
3. **`not`**: flips the value.
4. **Precedence**: `not` > `and` > `or`; use `()`.
5. **Short-circuit**: enables safe patterns like `x is not None and len(x)`.

---

# Expressions, statements & assignment operators

## Expressions vs statements (quick)

An **expression** is code that **evaluates to a value** (e.g. `2 + 3`, `age >= 18`, `name.upper()`, `a and b`). A **statement** is a full instruction Python executes (e.g. `x = 5`, `if x > 0:`, `print("hi")`, `pass`). **`if`** and **`while`** conditions use **expressions**; f-strings use **expressions** inside `{...}`.

```python
# Expressions (produce values)
total = 10 + 5
ok = age >= 18 and has_id

# Statements (do something / define structure)
score = 100
if score > 60:
    print(score)
```

## Assignment operators

Plain **`=`** assigns once. **Compound assignment** updates a variable using its current value:

| Operator | Example | Meaning |
|----------|---------|---------|
| `+=` | `n += 1` | `n = n + 1` |
| `-=` | `n -= 2` | `n = n - 2` |
| `*=` | `n *= 3` | `n = n * 3` |
| `/=` | `n /= 2` | `n = n / 2` (true division → float) |
| `//=` | `n //= 2` | `n = n // 2` |
| `%=` | `n %= 5` | `n = n % 5` |
| `**=` | `n **= 2` | `n = n ** 2` |

```python
count = 0
count += 1
discount = 10
discount += 5   # same idea as in nested discount examples
```

Still **assignment**, not comparison—don’t confuse **`+=`** (update) with **`==`** (equal test).

---

# Write If Statements

## Introduction

An **`if`** runs a block **only when** the condition is `True` — basic **control flow**. Before widespread high-level branching, many early programs ran straight through the same instructions every run; **conditional jumps** (what `if` compiles to) let the same program **choose paths** by data—still the core of “smart” behavior. **Analogy:** fork in the road, automatic door, or “if hungry, eat.”

---

<div align="center">

<div style="overflow: hidden; display: inline-block;">
  <img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.15.png"
       style="margin-top: -50px; display: block;"
       alt="Python if Statement Flowchart">
</div>

*If the condition is `True`, run the indented block; otherwise skip (unless you add `else` / `elif` later).*

</div>

---

## Syntax

```python
if condition:
    # indented block — runs only if condition is True
    pass
```

Parts: `if`, condition, `:`, then an **indented** block (convention: **4 spaces**).

## Examples

```python
age = 20
if age >= 18:
    print("You are an adult")  # prints

age = 15
if age >= 18:
    print("You are an adult")  # does not print
```

```python
print("Start")
if age >= 20:
    print("Adult branch")
print("End")  # always runs if reached
```

## Indentation

Python **requires** indentation for blocks; it is not optional.

```python
if age >= 18:
    print("A")
    print("B")      # same block
print("Always")     # outside if

# Errors: missing indent after colon, or mixing 4 vs 8 spaces inconsistently
if age >= 18:
    pass  # use pass for an intentionally empty block
```

## Conditions: comparisons, logic, booleans

```python
if temperature > 25:
    print("Hot")
if score >= 60:
    print("Passed")

if age >= 18 and has_license:
    print("Can drive")
if is_weekend or is_holiday:
    print("Sleep in")
if not form_submitted:
    print("Can edit")

if is_logged_in:
    print("Welcome")
if is_admin:  # if False, block skipped
    print("Admin")
```

## Multiple independent `if` statements

Each `if` is checked on its own; more than one block can run.

```python
score = 85
if score >= 60: print("Passed")
if score >= 70: print("C or better")
if score >= 80: print("B or better")
# All true branches run — unlike if/elif chain
```

## Quick real-world pattern

```python
age = int(input("Enter your age: "))
if age >= 18:
    print("Can create account")
if age >= 21:
    print("Premium available")
```

## Example: several checks on one input

Independent `if`s are useful when more than one message can apply (e.g. password feedback):

```python
password = input("Enter password: ")

if len(password) < 8:
    print("Password too short")
if len(password) >= 8:
    print("Password length OK")
if len(password) >= 12:
    print("Strong password!")
```

## Common mistakes

- **Missing `:`** after `condition`.
- **No indentation** under `if`.
- **`=` vs `==`**: `if age == 18` compares; `if age = 18` is a syntax error.
- **Wrong scope**: only indented lines belong to `if`; dedented lines always run.
- **Empty block**: use `pass`, not a blank body.

## Practice exercise

```python
x = 10
if x > 5:
    print("A")
    print("B")
if x > 15:
    print("C")
print("D")
```

<details>
<summary>Answer</summary>

Prints `A`, `B`, and `D`. `x > 5` is true; `x > 15` is false so `C` never prints. `D` is outside all `if` blocks.

</details>

## Key takeaways

1. **`if condition:`** plus indented block.
2. **Colon and indentation** are mandatory.
3. **Any boolean expression** can be the condition.
4. **Several `if`s** → independent checks; multiple branches may run.

---

# Write Elif Statements

## Introduction

**`elif`** checks **alternatives in order**; **only the first true branch** runs (unlike several separate `if`s). Fits multi-outcome decisions (grades A–F, traffic light state, temperature bands). **Analogy:** phone tree — after “press 2,” later options are skipped.

---

<div align="center">

<div style="overflow: hidden; display: inline-block;">
  <img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/images/1773052261494-94552dbe71da.jpg"
       style="margin-right: -40px; display: block;"
       alt="Python elif Multiple Conditions Flowchart">
</div>

*First matching condition wins; remaining `elif`s are skipped.*

</div>

---

## Why `elif` vs many `if`s

```python
score = 85
# Bad: every if runs; last assignment wins
if score >= 90: grade = "A"
if score >= 80: grade = "B"
if score >= 70: grade = "C"
# grade may end wrong

# Good: one branch, first match wins
if score >= 90: grade = "A"
elif score >= 80: grade = "B"
elif score >= 70: grade = "C"
else: grade = "F"   # see Else section
```

Syntax: `if` … one or more **`elif`** … optional **`else`**.

## Examples

```python
score = 75
if score >= 90: print("A")
elif score >= 80: print("B")
elif score >= 70: print("C")   # runs
elif score >= 60: print("D")

age = 15
if age >= 65: print("Senior")
elif age >= 18: print("Adult")
elif age >= 13: print("Teenager")  # runs
```

## Order matters

Check **more specific** conditions **before** general ones.

```python
score = 95
# Wrong: >= 60 catches everything including 95 first
# if score >= 60: "Pass"  elif score >= 90: "Excellent"  # Excellent never runs

# Right:
if score >= 90: print("Excellent")
elif score >= 60: print("Pass")
```

## Application: BMI bands

```python
bmi = 27.5
if bmi < 18.5: category = "Underweight"
elif bmi < 25: category = "Normal"
elif bmi < 30: category = "Overweight"
else: category = "Obese"
```

## Practice: `elif` vs many `if`s

```python
points = 120
# Version A — separate ifs: what is `tier` at the end? (Predict before running.)
tier = "bronze"
if points >= 100:
    tier = "gold"
if points >= 50:
    tier = "silver"
```

<details>
<summary>Hint</summary>

Both bodies can run; the **last** assignment wins — `tier` becomes `"silver"` even though `points` qualifies for gold. Use **`elif`** when tiers are exclusive.

</details>

## Example: traffic-style states

```python
light = "yellow"
if light == "red":
    action = "Stop"
elif light == "yellow":
    action = "Slow"
elif light == "green":
    action = "Go"
else:
    action = "Unknown"
```

## Key takeaways

1. **Mutually exclusive chain** (only one branch runs).
2. **`elif` must follow `if`**.
3. **First true condition wins** — order from specific to general.
4. **More efficient** than a pile of separate `if`s when outcomes are exclusive.

---

# Write Else Statements

## Introduction

**`else`** is the **default** when no prior `if`/`elif` matched — avoids “nothing happens” when you need a guaranteed response. **Analogies:** ATM wrong PIN, login failure, game wrong answer.

---

<div align="center">

<div style="overflow: hidden; display: inline-block;">
  <img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.17.png"
       style="margin-top: -100px; display: block;"
       alt="Python if-else Statement Flowchart">
</div>

*`else` runs when all previous conditions were false.*

</div>

---

## Syntax

```python
if cond:
    ...
else:
    ...

if c1: ...
elif c2: ...
else:
    # none of c1, c2 were true
    ...
```

**`else` has no condition** — it is not `else x > 0:`. One **`else`** per chain, and it must be **last** (never before `elif`).

## Examples

```python
age = 16
if age >= 18:
    print("Can vote")
else:
    print("Cannot vote yet")

# Full grade scale
score = 75
if score >= 90: grade = "A"
elif score >= 80: grade = "B"
elif score >= 70: grade = "C"
elif score >= 60: grade = "D"
else: grade = "F"
```

## When to use or skip `else`

Use when you need a **fallback**. Omit when you only care about certain cases and silence is OK.

```python
if age >= 18: print("Adult")
else: print("Minor")

if age >= 18: print("Adult")
# no else: under-18 prints nothing
```

## Applications

```python
if username == "admin" and password == "secret123":
    print("Login OK")
else:
    print("Invalid credentials")

age = 8
if age >= 65: price = 8
elif age >= 18: price = 12
elif age >= 5: price = 6
else: price = 0
```

## Common mistakes

```python
# Wrong — else has no condition
# else score < 60:
#     print("Fail")

# Correct
score = 55
if score >= 60:
    print("Pass")
else:
    print("Fail")
```

```python
# Wrong order of keywords — SyntaxError
# if score >= 90:
#     print("A")
# else:
#     print("below A")
# elif score >= 80:
#     print("B")

# Correct: all elifs, then else
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("Below B")
```

## Key takeaways

1. **`else`**: default, no condition.
2. **Last** in the chain; **one** per chain.
3. **Optional** but important when users need feedback on “all other cases.”

---

# Write Nested Conditionals

## Introduction

A **nested** conditional is an `if` **inside** another `if`’s block. Models **hierarchical** decisions (only check password **if** username matched; only alarm **if** motion **and** after hours). **Analogy:** boxes inside boxes, or turn-by-turn directions where later turns depend on earlier ones.

---

<div align="center">

![Python Nested if-else Conditional Control Flow](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.18.png)

*Each level adds a branch of the decision tree.*

</div>

---

## Syntax and motivation

Use nesting when a later check **only matters** if an earlier one is true.

```python
if age >= 18:
    if has_license:
        print("You can drive")
    else:
        print("Need a license")
else:
    print("Too young")

if username == "admin":
    if password == "secret":
        print("Login OK")
    else:
        print("Wrong password")
else:
    print("User not found")
```

## Deeper nesting

```python
if score >= 60:
    if submitted:
        if on_time:
            print("Full credit")
        else: print("Late penalty")
    else: print("Missing work")
else:
    print("Failed")
```

## Nested `if` vs `and`

```python
if age >= 18:
    if has_license:
        print("Can drive")
# Often equivalent for a single outcome:
if age >= 18 and has_license:
    print("Can drive")
```

Use **nesting** when **different actions** belong at different levels; use **`and`** when one combined condition is enough.

## Application: layered discount

```python
total, is_member, has_coupon = 150, True, True
if total >= 100:
    discount = 10
    if is_member:
        discount += 5
        if has_coupon:
            discount += 10
    print(f"Discount: {discount}%")
else:
    print("Below minimum for discount")
```

## Common mistakes

- **Too deep** — refactor with `and`/`or`, helpers, or **early exit** in functions (`if not ok: return`) so the “happy path” stays left-aligned and readable.
- **Wrong indentation** — inner `if` must be indented inside the outer block.
- **Equivalent flat form** — when both branches only need one combined condition, `if a and b` is often clearer than two nested `if`s.

## Key takeaways

1. **Inner checks** run only when **outer** condition holds.
2. **Indentation** reflects structure.
3. Prefer **flat** logic when it stays readable; **nest** when the story is truly hierarchical.

---

# Input & output: `input()` and `print()`

## Introduction

**`input()`** and **`print()`** are the usual pair for simple **console I/O**: read from the keyboard, show results in the terminal. Programs follow **input → processing → output**; this section covers both ends.

---

<div align="center">

![Python input() Function Diagram](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.9.jpg)

*`input()` returns a **string**; convert if you need numbers.*

</div>

---

## `print()` — showing output

`print` writes values to **standard output** (the console). You’ll use it for labels, debugging, and user-facing results—often with **f-strings**.

```python
print("Hello")
print("a", "b", "c")              # multiple values; default sep is a space
print("x", "y", sep=" | ")       # custom separator between arguments
print("No newline", end=" ")      # default end is "\n"; change to control line breaks
print(f"Score: {95}")
```

### How interactive programs fit in history

Early systems often used **batch** jobs (full input upfront, results later). **Command-line** interaction (type input, get a response) became standard from the 1960s onward and is still the foundation behind shells, REPLs, and tools that ask questions. **GUIs and web forms** are other kinds of input, but the same pipeline applies: capture data → process → show output.

## Basic usage

```python
name = input("Enter your name: ")
print("Hello, " + name + "!")
```

## Always a string

```python
age_str = input("Enter age: ")
print(type(age_str))  # <class 'str'>
age = int(age_str)
print("Next year:", age + 1)
```

**Why text first:** users can type anything; explicit **`int()`** / **`float()`** forces you to decide types and validate. Flexible for `"007"`-style input; validation-before-convert avoids crashes.

## Multiple values

```python
first = input("First: ")
last = input("Last: ")
age = int(input("Age: "))
print(f"{first} {last}, {age}")
```

## Practical snippets

```python
num1 = float(input("First number: "))
num2 = float(input("Second: "))
print("Sum:", num1 + num2)

name = input("Name: ")
city = input("City: ")
age = int(input("Age: "))
print(f"{name} from {city}, age {age}")
```

Interactive programs adapt per run instead of hardcoding `name = "Alice"`.

## Key takeaways

1. **`variable = input("prompt")`** — pauses until Enter.
2. **`print(...)`** — one or more values; optional **`sep=`**, **`end=`**.
3. **`input` always returns `str`** until you convert.
4. **Convert** with `int()`, `float()` when doing math.
5. **Clear prompts** help users; validate messy input in real apps.

---

# Format Output with F-strings

## Introduction

**F-strings** (`f"..."`, PEP 498, Python 3.6+) embed expressions in strings — **string interpolation**. They are usually the best default in modern Python.

### How Python string formatting evolved (short)

| Era | Style | Typical use |
|-----|--------|-------------|
| Early | `"Hi " + name + ", " + str(age)` | Simple but noisy and error-prone |
| C-style | `"Hi %s, %d" % (name, age)` | Powerful; easy to mix up `%s` / `%d` |
| `.format()` | `"Hi {}, you are {}".format(name, age)` | Clearer than `%`, still a bit long |
| 3.6+ | `f"Hi {name}, you are {age}"` | **Readable, fast, standard now** |

---

<div align="center">

![Python f-string Formatting](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.10.png)

*Expressions inside `{...}` are evaluated when the string is built.*

</div>

---

## Basics

```python
name, age = "Alice", 25
print(f"Hello, {name}! You are {age} years old.")

first, last, age = "John", "Doe", 30
print(f"{first} {last} is {age}")
```

## Expressions inside `{ }`

```python
price, quantity = 10, 3
print(f"Total: ${price * quantity}")

name = "alice"
print(f"Welcome, {name.upper()}!")

age = 20
print(f"Adult: {age >= 18}")
```

## Format specifiers (numbers)

```python
pi = 3.14159265
print(f"{pi:.2f}")    # 2 decimals
print(f"{pi:.4f}")

n = 42
print(f"{n:5}")     # width 5, default align
print(f"{n:<5}")    # left
print(f"{n:^5}")    # center

print(f"{1000000:,}")  # 1,000,000
```

## Practical examples

```python
item, price, qty = "Coffee", 4.50, 2
total = price * qty
print(f"Item: {item}\nPrice: ${price:.2f}\nQty: {qty}\nTotal: ${total:.2f}")

name = "Alice Johnson"
m, e = 95, 87
avg = (m + e) / 2
print(f"{name}\nMath: {m}\nEnglish: {e}\nAverage: {avg:.1f}")
```

## Comparing styles

```python
# Concatenation — easy to forget str()
msg = "Hi " + name + ", " + str(age)
# .format
msg = "Hi {}, {}".format(name, age)
# F-string
msg = f"Hi {name}, {age}"
```

**Zen:** readability counts — f-strings make template vs data obvious.

### Literals: braces and quotes

Use **`{{`** and **`}}`** when you want literal curly braces in the output. Inside `{...}`, use **matching quote types** for strings (e.g. `f"He said {'hi'}"`) so the parser does not close the f-string early.

### Quick conversion template

```python
c = 25
f = c * 9 / 5 + 32
print(f"{c}°C = {f:.1f}°F")
```

## Key takeaways

1. Prefix string with **`f`**; use **`{expr}`** for values and calculations.
2. **Format specs**: `:.2f` (decimals), `:,` (thousands), `:<5` / `:^5` (alignment).
3. Prefer f-strings in new Python 3.6+ code unless maintaining legacy formatting.
4. **`{{` / `}}`** for literal braces when needed.

---

## Putting the session together

Real scripts usually chain: **read** with `input()` → **convert** (`int`/`float`) → **decide** with `if` / `elif` / `else` and **logical** operators → **report** with f-strings.

```python
age_str = input("Age: ")
age = int(age_str)

if age < 0:
    print("Invalid age")
elif age < 13:
    group = "child"
elif age < 18:
    group = "teen"
elif age < 65:
    group = "adult"
else:
    group = "senior"

can_vote = age >= 18 and age <= 120
print(f"You are a {group}; can vote: {can_vote}")
```

This uses **nested ideas only where needed** (here a flat `if/elif` chain is enough). For “check B only if A,” use **nesting** or combine with **`and`**.

---

## Vocabulary

| Term | Meaning |
|------|---------|
| Expression | Code that evaluates to a value (e.g. `x + 1`, `a and b`) |
| Statement | A full instruction (e.g. assignment, `if`, `print(...)`) |
| Boolean | `True` or `False` (result of comparisons and logic) |
| Condition | Expression in `if` / `while` that must be truthy/falsy |
| Block | Indented lines “owned” by `if`, `elif`, `else`, loops, `def`, etc. |
| `elif` | “Else if”: next test only if previous `if`/`elif` failed |
| Short-circuit | `and`/`or` may skip evaluating the right side |
| Precedence | Rules for which operation binds first without `()` |
| Truthy / falsy | Values treated as True/False in condition context (e.g. `""` is falsy) |
| Interpolation | Embedding values inside a string (f-strings do this) |

## Common errors — quick lookup

| Symptom | Usual cause |
|---------|-------------|
| `IndentationError` after `if` | Missing indented body or mixed spaces/tabs |
| `SyntaxError` on `if age = 18` | Used assignment `=` instead of compare `==` |
| Wrong use of `+=` vs `==` | `+=` updates a variable; `==` only compares |
| `if` never seems to run | Condition is false; check values with `print` |
| `elif` never runs | An earlier condition is always true first — **reorder** |
| `TypeError` on `age + 1` after `input` | Forgot `int()` / `float()` — input is a **string** |
| Wrong grade / tier with `elif` | Same as ordering: broad check before specific |
| Surprise with `and` / `or` | Add `()`; remember `not` binds before `and`/`or` |

When something is wrong, **print the variables** just before the `if` and trace which branch you expect.

---

## Concept checklist (nothing dropped)

| Topic | Ideas kept |
|-------|------------|
| Logical operators | `and` / `or` / `not`, truth behavior, combining, precedence, short-circuit, range chaining, validation, `or` defaults, pitfalls (`&`/`|`, messy precedence, `== True`) |
| `if` | Syntax, indentation, comparisons + logic + boolean vars, multiple independent `if`s, flow, errors (`:`, `=`, scope, `pass`) |
| `elif` | vs stacked `if`s, first match, ordering, grades / age / BMI-style bands |
| `else` | default branch, no condition, position, optional use, login / pricing |
| Nesting | when to nest, multi-level example, vs `and`, discounts, “too deep” |
| Expressions / statements | value vs full instruction; where each appears |
| Assignment operators | `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=` |
| `input()` / `print()` | prompt + always `str`; `print` args, `sep`/`end`, conversion patterns |
| F-strings | syntax, expressions, numeric formats, alignment, thousands, receipt/report, vs `+` and `.format()`, escapes |

---

## Optional self-drills

1. **Logic:** Write one expression that is `True` only when `x` is strictly between 10 and 20 (use chaining or `and`).
2. **`if`:** Read two numbers with `input`, convert to `float`, and print which is larger (handle equality with a third message).
3. **`elif`:** Map test score to letter grade with a correct chain; test a score that would break the chain if `>= 60` were checked before `>= 90`.
4. **`else`:** Prompt for a username; if it matches `"admin"`, print “welcome admin”; otherwise print “unknown user”.
5. **Nesting:** Ask for age and a yes/no string for “parent present”; allow entry to a 15+ only event if adult **or** (minor **and** parent present says yes).
6. **I/O + f-string:** Ask for name and birth year, compute rough age with the current year, and print one f-string summary line.
7. **`print`:** Print three words on one line with `sep=" • "`. Print two parts on one line with no newline between them using `end`.
8. **Assignment:** Start `total = 100`; use `*=` to apply a 10% increase in one line and `print` the result.

These reuse the same ideas as the notes without adding new language features.

---
