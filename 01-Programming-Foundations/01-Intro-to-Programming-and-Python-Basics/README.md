# Introduction to Programming, Python Basics & Development Env Setup

## Session Objective
- Configuring a professional local environment
- Navigating the terminal confidently
- Executing your first Python script

## Agenda – Subtopics
1. **Python Setup** – Installing Python, working with VS Code and Terminal, writing and executing Python programs
2. **Core Fundamentals** – Variables and data types; operators (arithmetic, comparison)

---

# Development Environment Setup

## Installing VS Code

**Visual Studio Code (VS Code)** is a free code editor used by developers worldwide. Think of it like Microsoft Word, but for writing code instead of documents.

### Download & Install
- **Download link**: [https://code.visualstudio.com/download](https://code.visualstudio.com/download)
- Select the installer for your operating system (Windows, macOS, or Linux)
- Run the installer and follow the steps

### Important: Installation Options
During installation, **keep these options checked** (tick the boxes):

| Option | What it does |
|--------|--------------|
| **Add "Open with Code" action** | Lets you right-click any folder and open it in VS Code directly |
| **Enable Auto Save** | After install, go to **File → Auto Save** and turn it on. Your code saves automatically, so you don’t lose work |

---

<div align="center">

![VS Code Installation](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/session1/vscode-installation.png)

*VS Code – Download and installation steps*

</div>

---

## Installing Python

**Python** is the programming language we will use. Your computer needs Python installed to run Python programs.

### Download & Install
- **Download link**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Download the latest stable version (e.g., Python 3.12 or 3.13)
- Run the installer

### Critical Step: Add Python to PATH
During installation, **check the box "Add Python to PATH"**. This allows you to run Python from the terminal. If you skip this, you may get errors when running Python later.

### Verify Installation
After installing, **close and reopen** your terminal, then type:
```bash
python3 --version
```
You should see something like `Python 3.12.0`. If you see a version number, Python is installed correctly.

**If you get an error** like "python3 is not recognized": You may have skipped "Add Python to PATH". Re-run the Python installer and make sure that option is checked.

---

<div align="center">

![Python Installation](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/session1/python-installation.png)

*Python – Download and installation with "Add to PATH" option*

</div>

---

## Working with the Terminal

### What is the Terminal?
The **terminal** (also called command line or command prompt) is a window where you type text commands instead of clicking buttons. It’s like having a conversation with your computer.

### Why Do We Need It?
- To run Python programs
- To install packages and tools
- Professionals use it daily for development

### What Exactly Does the Terminal Do?
When you type `python3 index.py` and press Enter, the terminal:
1. Finds Python on your computer
2. Opens your file `index.py`
3. Runs the code line by line
4. Shows the output (results) on the screen

### Writing and Executing Your First Python Program

**Step 1:** Open VS Code and create a new file. Save it as `index.py` (the `.py` means it’s a Python file).

**Step 2:** Type this code in the file:
```python
print("Hello, World!")
```

**Step 3:** Save the file (or rely on Auto Save).

**Step 4:** Open the terminal in VS Code: click **Terminal → New Terminal** (or press `Ctrl+\`` on Windows/Linux, `Cmd+\`` on Mac).

**Step 5:** In the terminal, type:
```bash
python3 index.py
```
Press Enter.

You should see `Hello, World!` printed in the terminal. You have just run your first Python program.

---

<div align="center">

![Running Python in Terminal](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/session1/running-in-terminal.png)

*Running `python3 index.py` in the terminal – output appears below*

</div>

---

### Terminal: Do's and Don'ts

The terminal works differently from clicking files. Here’s what to watch for.

#### Do's

| Do | Reason |
|----|--------|
| **Make sure the terminal is in the right folder** | Python looks for `index.py` in the folder where the terminal is. If you're in the wrong folder, you'll get "No such file or directory" |
| **Use `cd` to move to your project folder first** | Type `cd` followed by the folder path. For example: `cd Desktop/myproject` |
| **Open VS Code from the folder** | Right-click the folder containing your `.py` file → "Open with Code". The terminal will start in that folder |
| **Check the path shown in the terminal** | Before `python3 index.py`, the line usually shows your current folder. That folder should contain your file |

#### Don'ts

| Don't | What goes wrong |
|-------|-----------------|
| **Don’t run `python3 index.py` from the wrong folder** | The terminal can’t find `index.py` and shows "No such file or directory" |
| **Don’t forget to save before running** | If Auto Save is off, unsaved changes won’t run. Save (Ctrl+S / Cmd+S) then run |
| **Don’t use spaces in file names** | `my file.py` can cause issues. Prefer `my_file.py` |
| **Don’t mix up `python` and `python3`** | On Mac/Linux, use `python3`. On some Windows setups you may use `python`. Stick to what works on your system |

#### Example: When the terminal is in the wrong place

```bash
# You're in your home folder, but index.py is on Desktop
$ python3 index.py
python3: can't open file 'index.py': [Errno 2] No such file or directory

# Fix: Navigate to the correct folder first
$ cd Desktop/myproject
$ python3 index.py
Hello, World!
```

---

# Understanding Syntax

## What is Syntax?

**Syntax** is the set of rules for how you write code. Like grammar in a language – if you break the rules, the computer can’t understand you and reports an error.

Python is strict about syntax. A missing colon, wrong indentation, or a typo can stop your program from running.

## Why Syntax Matters

The computer doesn’t infer what you meant. It only follows the exact rules. If the syntax is wrong, Python refuses to run the code and points to the line with the problem.

## Good Examples vs Bad Examples

### Example 1: Quotes for Strings

**Good:**
```python
name = "Alice"
message = 'Hello'
```

**Bad:**
```python
name = Alice          # Error! Python thinks Alice is a variable, not text
message = "Hello      # Error! Missing closing quote
```

### Example 2: Assignment Direction

**Good:**
```python
score = 100
age = 25
```

**Bad:**
```python
100 = score            # Error! Cannot assign to a number – variable must be on the left
25 = age               # Error! Same mistake – value on left, variable on right
```

### Example 3: Indentation (Python-Specific)

**Good:**
```python
if score > 50:
    print("Passed")   # Indented under if
```

**Bad:**
```python
if score > 50:
print("Passed")       # Error! Must be indented
```

### Example 4: Common Typos

**Good:**
```python
print("Hello")
```

**Bad:**
```python
Print("Hello")        # Error! Python is case-sensitive: print ≠ Print
pront("Hello")        # Error! Typo in function name
```

### What Happens When Syntax is Wrong?

Python shows a **SyntaxError** and highlights the line. Read the message carefully – it usually tells you what’s wrong. Fix that line and try again.

---

# Variables

---

<div align="center">

![Python Variables Memory Diagram](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.1.png)

*Variables are named references to objects — Python's type hierarchy shows all the types a variable can hold*

</div>

---

## What are Variables?

A **variable** is a named container that stores a value. Think of it like a locker at school: the locker number is the variable name, and the contents inside are the value. You can put something in, take it out, or change it later.

Variables give programs **memory** – they let you store data and use it again.

### The Assignment Operator (`=`)

We create variables using `=`:

```python
score = 100
name = "Alice"
age = 25
```

**Important:** Read `score = 100` as "score is assigned 100". The variable name goes on the **left**, the value on the **right**. The `=` means "assign", not "equals" in math.

### Using and Changing Variables

```python
score = 100
print(score)  # Output: 100

score = 75    # We can change it – that's why it's called a "variable"
print(score)  # Output: 75
```

### Variable Naming Rules

---

<div align="center">

![Python PEP 8 Naming Convention snake_case camelCase](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.2.png)

*PEP 8 naming conventions (snake_case for variables, UPPER_CASE for constants) keep Python code consistent and readable*

</div>

---

- Start with a letter or underscore
- Use only letters, numbers, and underscores
- In Python we use **snake_case**: `student_name`, `total_score`

### Using Variables in Calculations

Once you create variables, you can use them in expressions:

```python
price = 100
quantity = 3
total = price * quantity
print(total)  # 300

score = 100
bonus = 50
score = score + bonus   # Update score: add bonus to current value
print(score)            # 150
```

**Shorthand:** Python lets you write `score += 50` instead of `score = score + 50`. Same for `-=`, `*=`, etc. This is called *augmented assignment*.

### Common Mistake

```python
print(name)  # Error! We haven't created 'name' yet
name = "Alice"
print(name)  # Correct – create first, then use
```

---

# Data Types

## Why Do We Have Different Data Types?

You might wonder: why can’t we use one common type for everything? The answer is that different kinds of data need different treatment.

**Numbers need math.** If you store `price = 19.99`, you want to multiply it by quantity, add tax, round to 2 decimals. The computer needs to know it’s a number so it can do arithmetic.

**Text needs different handling.** A name like `"Alice"` shouldn’t be multiplied or divided. You might want to join it with another string (`"Hello, " + name`) or get its length. Numbers and text are used in different ways.

**A practical example:** Imagine a shopping app. The product name is text (`"Blue Shirt"`). The price is a number with decimals (`19.99`). The quantity is a whole number (`3`). If everything were stored as one type, the program wouldn’t know whether `"19"` means the number 19 or the text “19” – and `"19" * 3` would repeat “19” three times instead of calculating 57. Types tell the computer how to use each value correctly.

**Why separate int and float?** Integers are for counting (3 apples, 10 students). Floats are for measurements (19.99 rupees, 5.5 feet). Using the right type keeps calculations accurate and avoids confusion when dividing (e.g. `10 // 3` gives 3 for whole parts, `10 / 3` gives 3.33 for precise division).

---

<div align="center">

![Python Data Types Overview](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.3.jpg)

*Integers (int) are part of Python's numeric type hierarchy — whole numbers with unlimited precision*

</div>

---

The main types we use:

| Type | Example | Use |
|------|---------|-----|
| `int` | `25`, `-10` | Whole numbers |
| `float` | `19.99`, `3.14` | Numbers with decimals |
| `str` | `"Hello"` | Text |
| `bool` | `True`, `False` | Yes/no values |

## Integers (`int`)

Whole numbers with no decimal point:

```python
age = 25
score = 100
```

## Floats (`float`)

---

<div align="center">

![Python Float Object Diagram](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.4.png)

*Floats represent decimal numbers using IEEE 754 standard — essential for measurements and calculations*

</div>

---

Numbers with decimal points. Used for prices, measurements, percentages:

```python
price = 19.99
percentage = 87.5
```

**Note:** Division (`/`) always returns a float. So `10 / 2` gives `5.0`, not `5`.

**Mixing int and float:** When you add an integer and a float, the result is always a float:

```python
age = 25      # int
height = 5.8  # float
# age + height would give 30.8 (float)
```

## Strings (`str`)

---

<div align="center">

![Python String Character Indexing](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.5.png)

*Strings are immutable sequences of characters — Python provides rich methods for working with text*

</div>

---

Strings store text. Use single or double quotes:

```python
name = "Alice"
message = 'Hello, World!'
```

To join strings, use `+`:

```python
greeting = "Hello, " + name
print(greeting)  # Hello, Alice
```

**You cannot mix strings and numbers directly:** `"Age: " + 25` gives an error. Use `str(25)` to convert: `"Age: " + str(25)`.

## Booleans (`bool`)

---

<div align="center">

![Python Boolean True False Values](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.6.jpg)

*Booleans (True/False) are the foundation of logic — used in conditions, comparisons, and control flow*

</div>

---

Only two values: `True` or `False`. Used for yes/no logic:

```python
is_active = True
is_passing = False
```

## Checking Type

---

<div align="center">

![Python type() Function Dynamic Typing](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.7.jpg)

*type() reveals where a value sits in Python's type hierarchy — int, float, str, bool, and more*

</div>

---

Use `type()` to see what type a value is:

```python
score = 100
print(type(score))  # <class 'int'>

name = "Alice"
print(type(name))   # <class 'str'>
```

When you get a `TypeError`, `type()` helps you find the cause. For example, if `age` is accidentally the string `"25"` instead of the number `25`, adding `age + 5` will fail. Use `type(age)` to check, then convert with `int(age)` if needed.

---

# Arithmetic Operators

---

<div align="center">

![Python Arithmetic Operations Diagram](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.11.png)

*Python's arithmetic operators (+, -, *, /, //, %, **) map directly to fundamental mathematical operations*

</div>

---

Python uses symbols for math operations:

| Operator | Name | Example |
|----------|------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division | `10 / 2` → `5.0` |
| `//` | Integer division | `10 // 3` → `3` |
| `%` | Remainder | `10 % 3` → `1` |
| `**` | Power | `2 ** 3` → `8` |

### Example

```python
score = 100
bonus = 50
total = score + bonus
print(total)  # 150

price = 50
quantity = 3
subtotal = price * quantity
print(subtotal)  # 150
```

- **Division** (`/`) always gives a float
- **Integer division** (`//`) drops the decimal part
- **Modulo** (`%`) gives the remainder (e.g. `10 % 3` is 1)

### Integer Division vs Division

The difference often causes confusion. Try both:

```python
print(10 / 3)   # 3.333... (float – keeps decimal)
print(10 // 3)  # 3 (int – drops the decimal part)
```

Use `/` when you need decimals (e.g. averages). Use `//` when you need whole numbers (e.g. splitting 100 rupees among 3 people: 33 each).

### Modulo – A Practical Use

Modulo gives the remainder. Useful for checking even/odd:

```python
number = 10
print(number % 2)  # 0 – no remainder, so 10 is even

number = 7
print(number % 2)  # 1 – remainder 1, so 7 is odd
```

---

# Operator Precedence

---

<div align="center">

![Python Operator Precedence Table](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.12.jpg)

*Python follows PEMDAS/BODMAS rules: Parentheses → Exponents → Multiplication/Division → Addition/Subtraction*

</div>

---

## What is Operator Precedence?

When you write `2 + 3 * 4`, should Python do addition first (2+3=5, then 5*4=20) or multiplication first (3*4=12, then 2+12=14)? Without rules, the same expression could mean different things.

**Operator precedence** is the rule that decides which operation happens first. Python follows the same order as standard math: **PEMDAS**.

- **P**arentheses `()`
- **E**xponents `**`
- **M**ultiplication, **D**ivision `*`, `/`, `//`, `%`
- **A**ddition, **S**ubtraction `+`, `-`

## Examples

```python
# Multiplication happens before addition
result = 2 + 3 * 4
# Step 1: 3 * 4 = 12
# Step 2: 2 + 12 = 14
print(result)  # 14

# Use parentheses to change the order
result = (2 + 3) * 4
# Step 1: 2 + 3 = 5
# Step 2: 5 * 4 = 20
print(result)  # 20

# Another example: exponents first
result = 2 + 3 ** 2
# Step 1: 3 ** 2 = 9
# Step 2: 2 + 9 = 11
print(result)  # 11
```

## Why Order of Operations Matters

The expression `2 + 3 * 4` gives 14, not 20. If a calculation gives an unexpected result, check the order of operations. When unsure, use parentheses to make your intent clear:

```python
# Clear: we want (price * quantity) first, then add tax
total = (price * quantity) + tax
```

---

# Comparison Operators

Comparison operators are the foundation of **decision-making** in programs. They let code ask questions (e.g. Is score passing? Is age >= 18?) and respond based on the answer. Without them, programs would run the same instructions every time – no branching, no logic.

Every useful program uses comparisons: ATMs check if the balance is sufficient, games check if health > 0, login systems check if the password matches.

---

<div align="center">

![Python Comparison Operators Table](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.13.png)

*Comparison operators evaluate to True or False, enabling programs to branch into different paths*

</div>

---

## The Six Comparison Operators

Comparison operators compare two values and return a **boolean** result: `True` or `False`.

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `3 <= 5` | `True` |

## Examples

### Equal To (`==`) and Not Equal To (`!=`)

```python
age = 18
print(age == 18)  # True
print(age == 20)  # False

status = "pending"
print(status != "completed")  # True
print(status != "pending")     # False
```

### Greater Than, Less Than, Greater or Equal, Less or Equal

```python
score = 85
print(score > 75)   # True
print(score > 90)   # False
print(score >= 85)  # True (equal counts for >=)

age = 18
print(age >= 18)  # True – can vote
print(age >= 21)  # False – not yet 21
```

### Storing Comparison Results

Comparisons return boolean values, which you can store in variables:

```python
age = 20
is_adult = age >= 18
print(is_adult)        # True
print(type(is_adult))  # <class 'bool'>

score = 85
is_passing = score >= 60
is_excellent = score >= 90
print(is_passing)    # True
print(is_excellent)  # False
```

## Comparing Different Types

**Numbers:** You can compare integers and floats.

```python
print(5 == 5.0)      # True
print(10 > 9.5)      # True
```

**Strings:** Compared alphabetically. Case matters: `"ABC" != "abc"`.

**Type mismatch:** Don't compare incompatible types without converting.

```python
print(5 == "5")   # False – number vs string
# print(10 < "20")  # TypeError in Python 3
```

## Common Mistake: `=` vs `==`

```python
# Wrong – assigns 18 to age, doesn't check
if age = 18:   # SyntaxError!

# Correct – checks if age equals 18
if age == 18:
    print("Adult")
```

**Common mistake:** Use `==` for comparison, not `=`. The single `=` is for assignment.

---

# Common Mistakes and How to Avoid Them

These issues come up often. Here’s a quick reference:

| Mistake | What happens | Fix |
|---------|---------------|-----|
| **`=` vs `==`** | `if score = 60:` gives SyntaxError | Use `==` for comparison: `if score == 60:` |
| **Wrong folder in terminal** | "No such file or directory" | Run `cd` to your project folder first, then `python3 index.py` |
| **Unquoted text** | `name = Alice` – NameError | Use quotes: `name = "Alice"` |
| **Mixing strings and numbers** | `"Total: " + 100` – TypeError | Convert: `"Total: " + str(100)` |
| **Wrong precedence** | `2 + 3 * 4` gives 14, not 20 | Use parentheses: `(2 + 3) * 4` if you want 20 |
| **Forgot to save** | Old code runs | Save (Ctrl+S / Cmd+S) before running |

When you get an error, read the message. It usually points to the line and type of problem. Use `type()` to check variable types when you’re unsure.

---

# Key Takeaways

1. **Setup:** Install VS Code and Python. Add Python to PATH. Enable Auto Save in VS Code.
2. **Terminal:** Use it to run `python3 index.py` and see your program’s output.
3. **Variables:** Named containers for values. Use `=` to assign.
4. **Data types:** `int`, `float`, `str`, `bool`.
5. **Arithmetic:** `+`, `-`, `*`, `/`, `//`, `%`, `**`.
6. **Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=` – all return True or False.
7. **Operator precedence:** Python uses PEMDAS. Use parentheses when order matters.
8. **Terminal:** Ensure you're in the correct folder before running `python3 index.py`.
9. **Syntax:** Follow Python's rules exactly – quotes for strings, variable on left of `=`, correct indentation.

---

# Debugging Tips

When something goes wrong, check these in order:

| Problem | What to check |
|---------|---------------|
| "No such file or directory" | Terminal is in the wrong folder. Use `cd` to navigate to where your `.py` file is |
| "python3 is not recognized" | Python not in PATH. Reinstall Python with "Add to PATH" checked |
| SyntaxError | Missing quote, wrong indentation, typo. Read the line Python points to |
| TypeError (e.g. "can't add str and int") | Mixing types. Use `str()` or `int()` to convert before operations |
| Wrong calculation result | Check operator precedence. Add parentheses to force the order you want |

---

# Practice Exercise

Create `index.py` and try:

```python
score = 80
bonus = 20
total = score + bonus

print("Total score:", total)
print("Passing?", total >= 60)
```

Run it with `python3 index.py` and check the output.

**Challenge:** Modify the code to use `2 + 3 * 4` in a variable. Print it. Then change it to `(2 + 3) * 4` and see how the result differs. This reinforces operator precedence.

---

# Quick Reference

| Topic | Key points |
|-------|------------|
| **Terminal** | `cd folderpath` to navigate; must be in same folder as your `.py` file when you run `python3 index.py` |
| **Variables** | `name = value` – variable on left, value on right. Use snake_case. |
| **Data types** | `int` (whole), `float` (decimal), `str` (text in quotes), `bool` (True/False) |
| **Arithmetic** | `+` `-` `*` `/` `//` `%` `**` – `/` gives float, `//` gives int |
| **Comparison** | `==` `!=` `>` `<` `>=` `<=` – return True or False. Use `==` not `=` for equality. |
| **Precedence** | PEMDAS: Parentheses → Exponents → Mult/Div → Add/Sub. Use `()` to override. |
| **Syntax** | Quotes for strings, indentation matters, Python is case-sensitive |
