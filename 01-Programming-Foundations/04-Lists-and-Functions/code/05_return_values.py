# ============================================
# Return Values – Return Outputs from Functions
# ============================================


# --- Basic Return ---

def add(a, b):
    return a + b

result = add(5, 3)
print("add(5, 3):", result)             # 8


# --- Return a String ---

def make_greeting(name):
    return f"Hello, {name}!"

message = make_greeting("Alice")
print(message)                          # Hello, Alice!


# --- Return vs Print: The Critical Difference ---

def add_print(a, b):
    print(a + b)       # Displays to screen, returns None

def add_return(a, b):
    return a + b       # Sends value back to caller

print("\n--- Return vs Print ---")

result_print = add_print(5, 3)          # Displays: 8
print("result_print:", result_print)    # None — can't use it!

result_return = add_return(5, 3)        # No display
print("result_return:", result_return)  # 8 — can use it!

# With return, you can use the result in calculations
total = add_return(5, 3) * 2
print("add_return(5,3) * 2:", total)    # 16


# --- Multiple Return Statements ---

def check_number(num):
    if num > 0:
        return "Positive"
    elif num < 0:
        return "Negative"
    else:
        return "Zero"

print("\n--- Multiple Returns ---")
print("check_number(5):", check_number(5))     # Positive
print("check_number(-3):", check_number(-3))   # Negative
print("check_number(0):", check_number(0))     # Zero


# --- Return Exits the Function Immediately ---

def find_first_negative(numbers):
    for num in numbers:
        if num < 0:
            return num         # Exits here, rest of loop skipped
    return None                # Only reached if no negative found

print("\n--- Return Exits Immediately ---")
print("First negative:", find_first_negative([3, 7, -2, 9, -5]))  # -2
print("No negative:", find_first_negative([3, 7, 2, 9, 5]))       # None


# --- Returning Multiple Values ---

def get_min_max(numbers):
    return min(numbers), max(numbers)

smallest, largest = get_min_max([3, 1, 4, 1, 5, 9])
print(f"\n--- Multiple Return Values ---")
print(f"Min: {smallest}, Max: {largest}")   # Min: 1, Max: 9


# --- Function Composition (Chaining) ---

def double(x):
    return x * 2

def add_one(x):
    return x + 1

def square(x):
    return x ** 2

print("\n--- Function Composition ---")
result = add_one(double(5))
print("add_one(double(5)):", result)         # double(5)=10, add_one(10)=11

result = square(add_one(double(3)))
print("square(add_one(double(3))):", result) # double(3)=6, add_one(6)=7, square(7)=49


# --- Practical Examples ---

print("\n--- Practical Examples ---")

# Temperature converter
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

print(f"0°C = {celsius_to_fahrenheit(0)}°F")     # 32.0
print(f"100°C = {celsius_to_fahrenheit(100)}°F")  # 212.0

# Grade calculator
def calculate_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

scores = [95, 82, 67, 54, 73]
for score in scores:
    grade = calculate_grade(score)
    print(f"  Score {score} -> Grade {grade}")

# Using return value in a list comprehension
grades = [calculate_grade(s) for s in scores]
print(f"All grades: {grades}")
