# ============================================
# Strings – Implement Text Data Type
# ============================================


# --- Creating Strings ---

# Single or double quotes
name = 'Alice'
message = "He said, 'Hello!'"

# Multi-line strings
long_text = """This is a
multi-line string."""

print("name:", name)
print("message:", message)
print("long_text:", long_text)


# --- Strings Are Immutable ---

name = "Alice"
name = name.upper()   # Creates a NEW string, doesn't modify original
print("\nUppercase:", name)

# This would cause an error:
# name[0] = 'B'  # TypeError: 'str' does not support item assignment


# --- Character Encoding ---

# Python 3 uses Unicode by default
greeting = "Hello 世界 🌍"
print("\nUnicode:", greeting)

# Each character has a number
print("ord('A'):", ord('A'))     # 65
print("chr(65):", chr(65))       # 'A'


# --- String Concatenation (+) ---

first_name = "Alice"
last_name = "Johnson"
full_name = first_name + " " + last_name
print("\nConcatenation:", full_name)

# Must convert numbers to str before concatenating
age = 25
message = "Age: " + str(age)
print(message)


# --- String Repetition (*) ---

line = "=" * 20
print("\nRepetition:", line)

pattern = "Ha" * 3
print("Ha * 3:", pattern)        # HaHaHa


# --- String Length ---

name = "Alice"
length = len(name)
print(f"\nlen('{name}'):", length)  # 5


# --- String Indexing ---

name = "Alice"
print(f"\n'{name}' indexing:")
print("  name[0]:", name[0])     # A
print("  name[-1]:", name[-1])   # e
print("  name[1:4]:", name[1:4]) # lic


# --- Common String Methods ---

print("\n--- String Methods ---")

name = "  alice  "
print(f"strip().title(): '{name.strip().title()}'")  # 'Alice'

text = "Hello World"
print(f"replace: '{text.replace('World', 'Python')}'")

print(f"upper: '{'hello'.upper()}'")       # HELLO
print(f"lower: '{'HELLO'.lower()}'")       # hello

email = "user@example.com"
print(f"\nstartswith('user'): {email.startswith('user')}")  # True
print(f"endswith('.com'): {email.endswith('.com')}")         # True
print(f"'@' in email: {'@' in email}")                      # True


# --- split() and join() ---

sentence = "the cat sat on the mat"
words = sentence.split()
print(f"\nsplit(): {words}")

rejoined = " - ".join(words)
print(f"join(): '{rejoined}'")

csv_data = "apple,banana,cherry"
items = csv_data.split(',')
print(f"split(','): {items}")


# --- f-strings (Formatted Strings) ---

name = "Alice"
age = 25
score = 95.678

print(f"\n--- f-strings ---")
print(f"Name: {name}, Age: {age}")
print(f"Score: {score:.2f}")        # 2 decimal places
print(f"{'Centered':^20}")          # Center in 20 chars
print(f"{'Left':<20}|")             # Left align
print(f"{'Right':>20}|")            # Right align


# --- Practical Example ---

print("\n--- Practical Example ---")
first_name = "Alice"
last_name = "Johnson"
full_name = first_name + " " + last_name
initials = first_name[0] + last_name[0]

print(f"Full name: {full_name}")
print(f"Initials: {initials}")
print(f"Email: {full_name.lower().replace(' ', '.')}@example.com")


# --- Key Takeaways ---
# 1. Strings are text in quotes (single, double, or triple)
# 2. Immutable — any "change" creates a new string
# 3. + to concatenate, * to repeat
# 4. str() to convert numbers before concatenating
# 5. upper(), lower(), strip(), replace(), split(), join()
# 6. len() for length, in for membership check
