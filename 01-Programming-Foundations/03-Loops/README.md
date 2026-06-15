# Introduction to Loops

In everyday programs, the same kind of step often has to run **many times**: process every line in a file, every user in a list, every guess in a game, or every tick until a condition changes. Writing separate instructions for each repetition does not scale and is impossible when you do not know the count ahead of time. **Loops** solve this by letting you describe **once** what should repeat and **when** it should stop (or how many times to go).

## Why loops are needed

1. **Scale and length**: Ten steps or ten million steps can use the **same** few lines of code; you do not duplicate blocks by hand.
2. **Unknown counts**: You often repeat until something happens (“valid password”, “guess is correct”, “balance is zero”) rather than a fixed number you knew when you wrote the code.
3. **Consistency**: Every repetition runs the **same** logic, which reduces bugs and makes changes easy—you fix logic in one place.
4. **Working with collections**: Lists, strings, ranges, and other sequences are meant to be traversed; loops are the standard way to visit each item.

## What problems loops solve (in one line each)

| Situation | Without a loop | With a loop |
| --- | --- | --- |
| Same action N times | Copy-paste N times | One loop body, controlled by N or a condition |
| Process each item in data | Manual index and lots of branches | Clear “for each” or index-based iteration |
| Retry until input is valid | Awful nested `if` chains | Repeat until a condition becomes true |
| Search or scan until found | Must check every case explicitly | Stop early when found (with `break` where useful) |
| Tables and combinations | Cannot express row/column patterns | Nested loops express grids and pairs |

**Iteration** is the name for this pattern: executing a block of code repeatedly, usually with something changing each time (a counter, the next item in a list, or user input).

## What this session covers

Python gives you several loop-related tools. Later sections build on this idea in order:

- **While loops** — repeat **while** a Boolean condition is true (great for “until done” and validation).
- **For loops** — iterate over **sequences** (lists, strings, etc.) in a readable way.
- **`range()`** — produce numeric sequences efficiently for counting and indexing.
- **`break` and `continue`** — leave a loop early or skip one pass without rewriting the whole structure.
- **Nested loops** — outer and inner repetition for tables, grids, and combinations.

The rest of these notes keep that order; we start with **while** because it makes the **condition and update** very visible—then **for** and **range** feel like natural shortcuts for common cases.

---

# Write While Loops

## Introduction

While loops introduce **iteration** - the ability to repeat code automatically. This is one of the most powerful concepts in programming, transforming static instructions into dynamic, adaptive behavior.

---

<div align="center">

<div style="overflow: hidden; display: inline-block;">
  <img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.19.png" 
       style="margin-top: -40px; display: block;" 
       alt="Python while Loop Flowchart">
</div>

*A while loop checks its condition before each iteration — if True, the body executes; if False, the loop exits*

</div>
---

### The Power of Repetition

**Without loops**: To print "Hello" 100 times, you'd write `print("Hello")` 100 times!
**With loops**: Write it once, loop 100 times.

This concept revolutionized programming in the 1950s. Before loops, programmers had to manually duplicate code or use complex jump statements. Loops made programs exponentially more powerful.

### Real-World Analogy

While loops are like **"while" instructions in real life**:
- "While the laundry is wet, keep drying"
- "While there are dirty dishes, keep washing"
- "While the light is red, wait"

The action repeats until the condition changes. Programs work the same way!

## While Loops

A while loop repeats code **as long as** a condition is True.

### Basic Syntax

```python
while condition:
    # Code to repeat
    # Must eventually make condition False!
```

## Simple Examples

### Example 1: Count to 5

```python
count = 1

while count <= 5:
    print(count)
    count += 1

# Output: 1 2 3 4 5
```

### Example 2: User Input Validation

```python
password = ""

while len(password) < 8:
    password = input("Enter password (min 8 chars): ")

print("Password accepted!")
```

## Infinite Loops

**Warning**: If condition never becomes False, loop runs forever!

```python
# Infinite loop - BAD!
count = 1
while count <= 5:
    print(count)
    # Forgot to increment count!

# Correct
count = 1
while count <= 5:
    print(count)
    count += 1  # Makes condition eventually False
```

## Real-World Applications

### ATM Withdrawal

```python
balance = 1000

while balance > 0:
    print(f"Balance: ${balance}")
    amount = int(input("Withdraw amount (0 to quit): "))
    
    if amount == 0:
        break
    elif amount > balance:
        print("Insufficient funds")
    else:
        balance -= amount
        print(f"Withdrew ${amount}")

print("Thank you!")
```

### Number Guessing Game

```python
secret = 42
guess = 0

while guess != secret:
    guess = int(input("Guess the number: "))
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")

print("Correct!")
```

## Key Takeaways

1. **Repeats while True**: Loop continues as long as condition is True
2. **Must update**: Condition must eventually become False
3. **Check before run**: Condition checked before each iteration
4. **Infinite loops**: Dangerous if condition never becomes False
5. **Use for validation**: Great for user input validation


---

# Write For Loops

## Introduction

For loops introduce **iteration over collections** - the ability to process each item in a sequence automatically. This is one of Python's most elegant features, making data processing intuitive and concise.

### Why For Loops Are Revolutionary

**The problem with while loops**: Need manual counter management, index tracking, condition checking.
**For loops solution**: "For each item in this collection, do something" - natural, readable, Pythonic.

**Historical note**: Early languages (FORTRAN, 1957) had basic for loops. Python's for loop (1991) improved on this by iterating directly over collections, not just numbers - a game-changer for readability.

### Real-World Analogy

For loops are like **"for each" instructions**:
- "For each student in the class, mark attendance"
- "For each email in inbox, check if spam"
- "For each item in cart, calculate price"

You process the entire collection, one item at a time, automatically.

---
<div align="center">

<div style="overflow: hidden; display: inline-block;">
  <img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.22.png" 
       style="margin-bottom: -25px; display: block;" 
       alt="Python for Loop Flowchart Diagram">
</div>

*Flowchart of a for loop: the loop checks the sequence for remaining items, executes the body for each item, and exits when the sequence is exhausted*

</div>

---

## For Loops

A for loop iterates over a sequence (list, string, range, etc.).

### Basic Syntax

```python
for item in sequence:
    # Code using item
```

## Examples

### Example 1: Iterate String

```python
name = "Alice"

for letter in name:
    print(letter)

# Output: A l i c e (each on new line)
```

### Example 2: Iterate List

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry
```

# Output: 0 1 2 3 4

## For Loop vs While Loop

```python
# For loop - when you know iterations
for i in range(5):
    print(i)

# While loop - when condition-based
count = 0
while count < 5:
    print(count)
    count += 1
```

## Real-World Applications

### Validate All Inputs

```python
scores = [85, 92, 78, 95, 88]
all_passing = True

for score in scores:
    if score < 60:
        all_passing = False
        break

if all_passing:
    print("Everyone passed!")
```

### Process Each Item

```python
prices = [19.99, 29.99, 39.99]
tax_rate = 0.08

for price in prices:
    final_price = price * (1 + tax_rate)
    print(f"${price} -> ${final_price:.2f}")
```

## Key Takeaways

1. **Iterates sequences**: Works with lists, strings, ranges
2. **Automatic**: No manual counter needed
3. **Cleaner than while**: For known iterations
4. **item variable**: Automatically gets next value
5. **Use when**: You know what to iterate over


---

# Use Range Function

## Introduction

The `range()` function represents a crucial innovation in how programming languages handle **numeric iteration**. It introduces the concept of **lazy generation** - producing values on-demand rather than creating them all at once in memory.

### Why Range Exists

**The memory problem**: If you need to count from 1 to 1 million, creating a list of 1 million numbers wastes memory and time.
**Range solution**: Generate numbers one at a time, as needed. Only the current number exists in memory.

**Historical note**: Python 2 had `range()` (created a list) and `xrange()` (lazy generation). Python 3 simplified this - `range()` now always uses lazy generation, making it memory-efficient by default.

### Real-World Analogy

Range is like a **ticket dispenser machine**:
- Doesn't print all tickets upfront (memory waste!)
- Prints next ticket only when you press the button (on-demand)
- Knows the sequence (1, 2, 3...) but generates incrementally
- Can handle billions of tickets without running out of space

You get numbers one at a time, exactly when you need them.

### The Power of Lazy Evaluation

```python
# This doesn't create 1 billion numbers in memory!
for i in range(1000000000):
    if i == 5:
        break  # Exit early - only 6 numbers ever created
```

Range saves memory by generating values **just in time**. This is called **lazy evaluation** - a fundamental concept in efficient programming.

---

<div align="center">

![Python range() Function with for Loop](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.23.jpg)

*The range() function generates numbers on demand, enabling efficient numeric iteration without storing the entire sequence in memory*

</div>

---

## The Range Function

`range()` generates a sequence of numbers, commonly used with for loops.

### Three Forms

```python
range(stop)              # 0 to stop-1
range(start, stop)       # start to stop-1
range(start, stop, step) # start to stop-1, by step
```

## Examples

### Form 1: range(stop)

```python
for i in range(5):
    print(i)

# Output: 0 1 2 3 4 (stops before 5!)
```

### Form 2: range(start, stop)

```python
for i in range(2, 7):
    print(i)

# Output: 2 3 4 5 6 (stops before 7!)
```

### Form 3: range(start, stop, step)

```python
for i in range(0, 10, 2):
    print(i)

# Output: 0 2 4 6 8 (even numbers)
```

### Counting Down

```python
for i in range(5, 0, -1):
    print(i)

# Output: 5 4 3 2 1 (countdown)
```

## Real-World Applications

### Multiplication Table

```python
num = 5

for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")
```

### Year Range

```python
for year in range(2020, 2025):
    print(f"Year: {year}")

# Output: 2020 2021 2022 2023 2024
```

### Skip Every Third

```python
for i in range(0, 20, 3):
    print(i)

# Output: 0 3 6 9 12 15 18
```

## Range with Lists

```python
fruits = ["apple", "banana", "cherry"]

# Access by index
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# Output:
# apple
# banana
# cherry
```

## Key Takeaways

1. **Generates numbers**: Not a list, but a range object
2. **Stops before end**: range(5) goes 0 to 4, not 5
3. **Default start**: 0 if not specified
4. **Default step**: 1 if not specified
5. **Can count down**: Use negative step


---

# Control Loops with Break

## Introduction

The `break` statement stops a **while** or **for** loop immediately when a special condition is met. After `break`, execution continues with the first line **after** the loop—the main loop condition is not evaluated again for that exit.

### Why early exit matters

**The efficiency problem**: Without `break`, loops often keep running even after you have already found what you need or hit a fatal error.

**Flow control solution**: Exit early with `break`, saving time and making logic cleaner.

**Real-world impact**: Google's search doesn't check all 50 billion web pages when you search—it uses `break` to stop once it finds enough good results. Your loop can do the same!

### Selective iteration

Traditional approach processes everything:

```python
# Must check ALL items
for item in large_dataset:
    # Process even after finding what you need
```

With `break`:

```python
# Stop when done
for item in large_dataset:
    if found_target:
        break  # Save time!
```

This is **algorithmic efficiency**—doing less work for the same goal.

---

## The `break` statement

`break` exits the **current** loop immediately. It works in **while** and **for** loops.

---

<div align="center">

<div style="overflow: hidden; display: inline-block;">
  <img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.20.png" 
       style="margin-top: -50px; display: block;" 
       alt="Python break Statement Flowchart">
</div>

---

*The break statement exits the loop immediately — jumping straight past the loop body to the next statement*

</div>

---

### Why `break` exists

Sometimes you exit for reasons beyond the main loop condition:

- **Search**: Stop when the item is found
- **Validation**: Stop on first error
- **User quit**: Stop when the user says quit

Without `break`, you often need awkward condition combinations; with `break`, the intent stays clear.

### Real-world analogy

Break is like **"stop the search!"**—keys found, stop checking pockets; answer found, stop reading; alarm sounds, stop and evacuate.

### Basic syntax

```python
while condition:
    if some_condition:
        break  # Exit loop immediately
```

```python
for item in sequence:
    if some_condition:
        break
```

### Examples (while loops)

**Search and stop**

```python
numbers = [3, 7, 2, 9, 5]
target = 9
index = 0

while index < len(numbers):
    if numbers[index] == target:
        print(f"Found {target} at index {index}")
        break  # Stop searching
    index += 1
```

**Exit on command**

```python
while True:
    command = input("Enter command (or 'quit'): ")
    if command == "quit":
        break
    print(f"Executing: {command}")

print("Program ended")
```

**Password until correct**

```python
while True:
    password = input("Enter password: ")
    if password == "secret":
        break
    print("Wrong password!")
```

### Break vs loop condition

```python
# Using break
while True:
    x = int(input("Enter number (0 to stop): "))
    if x == 0:
        break
    print(f"You entered: {x}")

# Using the loop condition
x = -1
while x != 0:
    x = int(input("Enter number (0 to stop): "))
    if x != 0:
        print(f"You entered: {x}")
```

## Examples in `for` loops (`break`)

The same rules apply: one `break` exits **one** loop—the innermost loop that contains it.

### Break in a `for` loop

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in numbers:
    if num == 6:
        break  # Stop at 6
    print(num)

# Output: 1 2 3 4 5
```

### Find first match

```python
names = ["Alice", "Bob", "Charlie", "David"]
target = "Charlie"

for i in range(len(names)):
    if names[i] == target:
        print(f"Found {target} at index {i}")
        break
```

### Early exit on error

```python
data = [10, 20, 0, 40, 50]

for num in data:
    if num == 0:
        print("Error: Zero found!")
        break
    result = 100 / num
    print(f"100 / {num} = {result}")
```

## Key Takeaways

1. **`break`** exits the **current** loop immediately (`while` or `for`).
2. **Use for**: Search/stop, user quit, errors—whenever you are done and should not keep iterating.
3. **Nested loops** (later): `break` affects only the **innermost** loop around it.


---

# Control Loops with Continue

## Introduction

The `continue` statement **does not** exit the loop. It skips the rest of the **current** iteration and jumps to the **next** one—in both **while** and **for** loops.

### Why skipping matters

**The filtering problem**: You often want to ignore some items (bad input, values you do not need) but still process the rest.

**Continue in one sentence**: “Skip this iteration; keep the loop running.”

**Contrast with `break`**: `break` stops the whole loop; `continue` only skips one pass. See **`continue` vs `break`** below.

---

## The `continue` statement

`continue` skips the rest of the current iteration and goes to the next one.

---

<div align="center">

![Python continue Statement Flow Diagram](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.21.png)

*The continue statement skips the remaining loop body and jumps back to the condition check for the next iteration*

</div>

---

### Why `continue` exists

- **Filter while processing**: Skip invalid entries but keep going
- **Conditional skipping**: Ignore cases without stopping entirely
- **Cleaner logic**: Avoid deeply nested `if` statements

**Without continue**: Complex nested ifs. **With continue**: Clear, linear flow.

### Real-world analogy

Continue is like **"skip this, next!"**—defective item on the line, skip it; boring chapter, skip it; song you dislike, skip to next (playback keeps running).

### Basic syntax

```python
while condition:
    if some_condition:
        continue  # Skip to next iteration
```

```python
for item in sequence:
    if some_condition:
        continue
```

### Examples (while loops)

**Skip even numbers**

```python
count = 0

while count < 10:
    count += 1
    if count % 2 == 0:
        continue  # Skip even numbers
    print(count)  # Only prints odd numbers

# Output: 1 3 5 7 9
```

**Input validation**

```python
attempts = 0

while attempts < 5:
    age = int(input("Enter age: "))
    attempts += 1

    if age < 0:
        print("Invalid age!")
        continue  # Skip to next attempt

    print(f"Valid age: {age}")
    break
```

### `continue` vs `break`

```python
# continue — skips one iteration
count = 0
while count < 10:
    count += 1
    if count == 5:
        continue  # Skips printing 5
    print(count)

# break — exits the loop
count = 0
while count < 10:
    count += 1
    if count == 5:
        break  # Stops at 5
    print(count)
```

---

<div align="center">

![Python break vs continue Statement Flowchart](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.24.png)

*The break statement immediately exits the loop when a condition is met, while continue skips the current iteration and proceeds to the next one*

</div>

---

## Examples in `for` loops (`continue`)

### Continue in a `for` loop

```python
for num in range(1, 11):
    if num % 2 == 0:
        continue  # Skip even numbers
    print(num)

# Output: 1 3 5 7 9
```

### Filter while iterating

```python
scores = [95, 45, 87, 32, 91, 68]

for score in scores:
    if score < 60:
        continue  # Skip failing scores
    print(f"Passing score: {score}")

# Output: Passing score: 95, 87, 91, 68
```

## Before nested loops: `break` only exits the innermost loop

```python
# Break only exits innermost loop
for i in range(3):
    for j in range(3):
        if j == 2:
            break  # Exits inner loop only
        print(f"i={i}, j={j}")
```

## Key Takeaways

1. **`continue`**: Skips the rest of this iteration; the loop keeps running (`while` or `for`).
2. **`break`**: Exits the entire loop (see **Control Loops with Break**).
3. **Filtering**: Use `continue` when one bad or unwanted item should not stop the rest.
4. **Updates**: In `while` loops, still advance counters or read new input so you do not loop forever.
5. **Nested loops**: `break` and `continue` apply to the **innermost** loop that contains them.


---

# Write Nested Loops

## Introduction

Nested loops introduce **multi-dimensional iteration** - the ability to process data with multiple levels or dimensions. They represent a fundamental pattern in computing for handling **combinations**, **grids**, and **hierarchical data**.

### Why Nested Loops Exist

**The multi-level problem**: Real-world data isn't linear - think spreadsheets (rows AND columns), chess boards (8x8 grid), class schedules (students AND subjects).
**Nested loops solution**: One loop handles outer level (rows), inner loop handles inner level (columns).

**Computer graphics**: Every pixel on your screen was drawn using nested loops - one loop for rows, one for columns. Video games render millions of pixels per second using this pattern!

### Real-World Analogy

Nested loops are like **reading a book**:
- **Outer loop**: Iterate through each chapter (chapter 1, 2, 3...)
- **Inner loop**: Read each page in that chapter (page 1, 2, 3...)
- **Pattern**: For each chapter, you read ALL its pages before moving to next chapter

Or like **a teacher taking attendance**:
- **Outer loop**: Go through each row of seats
- **Inner loop**: Check each student in that row
- **Complete inner before advancing outer**: Check all students in row 1 before moving to row 2

### The Power of Combinations

Nested loops let you explore **all possible combinations**:
```python
# outer × 4 inner = 12 total combinations
for i in [1, 2, 3]:
    for j in ['A', 'B', 'C', 'D']:
        print(f"{i}{j}")  # 1A, 1B, 1C, 1D, 2A, 2B...
```

This **Cartesian product** is fundamental in mathematics, databases (SQL joins), and algorithms.

---

<div align="center">

![Python Nested Loops Diagram](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/9.1/LO-9.1.25.png)

*Nested loops place one loop inside another — the inner loop completes all iterations for each single iteration of the outer loop*

</div>

---

## Nested Loops

A nested loop is a loop inside another loop.

### Basic Syntax

```python
for outer_var in outer_sequence:
    for inner_var in inner_sequence:
        # Inner loop body
        # Runs completely for each outer iteration
```

## Simple Example

```python
for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")

# Output:
# i=0, j=0
# i=0, j=1
# i=1, j=0
# i=1, j=1
# i=2, j=0
# i=2, j=1
```

## Patterns

### Rectangle of Stars

```python
for row in range(3):
    for col in range(5):
        print("*", end="")
    print()  # New line after each row

# Output:
# *****
# *****
# *****
```

### Multiplication Table

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i}x{j}={i*j}", end="\t")
    print()

# Output: 5x5 multiplication table
```

### Right Triangle

```python
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()

# Output:
# *
# **
# ***
# ****
# *****
```

## Key Takeaways

1. **Loop in loop**: Inner loop completes for each outer iteration
2. **Multiply iterations**: Total = outer * inner
3. **Use for patterns**: Grids, tables, combinations
4. **Can nest multiple**: 3+ levels (but avoid too deep)
5. **break affects inner**: Only exits innermost loop


---

