# ============================================
# Functions – Define, Parameters & Defaults
# ============================================


# --- Defining a Simple Function ---

def say_hello():
    print("Hello, World!")

say_hello()
say_hello()  # Can call multiple times


# --- Function with Multiple Statements ---

def greet_user():
    print("Welcome!")
    print("Thanks for using our program")
    print("Have a great day!")

print()
greet_user()


# --- Function Naming (verb-based, descriptive) ---

def calculate_total():
    pass

def send_email():
    pass

def validate_input():
    pass

# Avoid: func1(), do_stuff(), x()


# --- Functions Calling Functions ---

def print_header():
    print("=" * 40)
    print("Welcome to My Program")
    print("=" * 40)

def print_footer():
    print("=" * 40)
    print("Thank you!")
    print("=" * 40)

def show_welcome():
    print_header()
    print("\nPlease choose an option:")
    print_footer()

print()
show_welcome()


# ============================================
# Function Parameters
# ============================================

# --- Single Parameter ---

def greet(name):
    print(f"Hello, {name}!")

print()
greet("Alice")
greet("Bob")


# --- Multiple Parameters ---

def add_numbers(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")

print()
add_numbers(5, 3)
add_numbers(10, 20)


# --- Parameters vs Arguments ---
# Parameter = variable in function definition
# Argument  = actual value passed when calling

def introduce(name, age):
    print(f"{name} is {age} years old")

print()
introduce("Alice", 25)    # Correct
introduce(25, "Alice")    # Wrong order! (still runs but makes no sense)


# ============================================
# Default Parameters
# ============================================

# --- Basic Default Parameter ---

def greet_with_default(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print()
print(greet_with_default("Alice"))              # Uses default
print(greet_with_default("Bob", "Hi"))          # Overrides default
print(greet_with_default("Charlie", greeting="Hey"))  # Keyword argument


# --- Multiple Defaults ---

def create_user(username, email, role="user", active=True):
    return {
        "username": username,
        "email": email,
        "role": role,
        "active": active
    }

print()
user1 = create_user("alice", "alice@example.com")
print("User 1:", user1)

user2 = create_user("bob", "bob@example.com", role="admin")
print("User 2:", user2)

user3 = create_user("charlie", "charlie@example.com", active=False)
print("User 3:", user3)


# --- Mutable Default Trap ---

# BAD: mutable default is shared between calls!
def add_item_bad(item, items=[]):
    items.append(item)
    return items

print()
print("BAD - mutable default:")
print("  Call 1:", add_item_bad(1))    # [1]
print("  Call 2:", add_item_bad(2))    # [1, 2] — Unexpected!

# GOOD: use None and create inside
def add_item_good(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print("\nGOOD - None default:")
print("  Call 1:", add_item_good(1))   # [1]
print("  Call 2:", add_item_good(2))   # [2] — Correct!


# --- Python's Own Functions Use Defaults ---

# print(value, sep=' ', end='\n')  — sep and end have defaults

print()
print(1, 2, 3)                  # 1 2 3 (default sep=' ')
print(1, 2, 3, sep=', ')        # 1, 2, 3 (custom sep)
print("no newline", end=' ')
print("same line")
