# ============================================
# Classes – __init__ Constructor & Initialization
# ============================================


# --- Why __init__? ---

# Without __init__: must set attributes manually (error-prone)
class DogBad:
    pass

dog = DogBad()
# dog.name  # AttributeError! Forgot to set it.


# With __init__: attributes are guaranteed
class DogGood:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

dog = DogGood("Buddy", "Labrador")
print(f"{dog.name} is a {dog.breed}")    # Buddy is a Labrador


# --- Basic Syntax ---

class ClassName:
    def __init__(self, param1, param2):
        self.attr1 = param1
        self.attr2 = param2


# --- The self Parameter ---

class Car:
    def __init__(self, brand, year):
        self.brand = brand    # THIS car's brand
        self.year = year      # THIS car's year

    def describe(self):
        return f"{self.year} {self.brand}"

car1 = Car("Toyota", 2020)
car2 = Car("Honda", 2021)

print(f"\ncar1: {car1.describe()}")    # 2020 Toyota
print(f"car2: {car2.describe()}")      # 2021 Honda
# self points to different objects for car1 vs car2


# --- __init__ Runs Automatically ---

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"  Student '{name}' created!")   # Proof it runs automatically

print("\nCreating students:")
s1 = Student("Alice", 22)    # __init__ runs automatically
s2 = Student("Bob", 24)      # __init__ runs automatically


# --- __init__ with Default Values ---

class Connection:
    def __init__(self, host, port=5432, timeout=30):
        self.host = host
        self.port = port
        self.timeout = timeout

conn1 = Connection("localhost")
conn2 = Connection("prod-db", port=3306, timeout=60)

print(f"\nconn1: {conn1.host}:{conn1.port} (timeout={conn1.timeout})")
print(f"conn2: {conn2.host}:{conn2.port} (timeout={conn2.timeout})")


# --- Validation in __init__ ---

class Person:
    def __init__(self, name, age):
        self.name = name or "Unknown"
        self.age = max(0, age)          # No negative ages

p1 = Person("Alice", 25)
p2 = Person("", -5)

print(f"\np1: {p1.name}, age {p1.age}")   # Alice, age 25
print(f"p2: {p2.name}, age {p2.age}")     # Unknown, age 0


# --- Derived / Computed Fields ---

class Employee:
    def __init__(self, name, hourly_rate, hours_worked):
        self.name = name
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
        self.salary = hourly_rate * hours_worked   # Computed!

emp = Employee("Alice", 50, 160)
print(f"\n{emp.name}'s salary: ${emp.salary}")     # $8000


# --- __init__ with No Parameters ---

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

counter = Counter()
counter.increment()
counter.increment()
counter.increment()
print(f"\nCounter: {counter.count}")    # 3

counter.reset()
print(f"After reset: {counter.count}")  # 0


# --- Constructor vs Regular Method ---

class TaskBad:
    def setup(self, name):          # Must call manually — can forget!
        self.name = name

class TaskGood:
    def __init__(self, name):       # Runs automatically — guaranteed!
        self.name = name

# task = TaskBad()
# task.name  # AttributeError — forgot to call setup()!

task = TaskGood("Deploy")
print(f"\nTask: {task.name}")        # Always works


# ============================================
# Common Mistakes
# ============================================

print("\n" + "=" * 40)
print("COMMON MISTAKES")
print("=" * 40)

# MISTAKE 1: name = name instead of self.name = name
class DogMistake1:
    def __init__(self, name):
        name = name           # Local variable only! Lost after __init__
        # self.name = name    # CORRECT

dog = DogMistake1("Buddy")
# dog.name  # AttributeError!
print("\nMistake 1: 'name = name' is local only (use self.name = name)")


# MISTAKE 2: Forgetting self parameter
# class DogMistake2:
#     def __init__(name):      # Missing self!
#         self.name = name     # TypeError on creation

print("Mistake 2: Always include 'self' as first parameter")


# MISTAKE 3: Wrong indentation
# class DogMistake3:
# def __init__(self, name):    # Not indented inside class!
#     self.name = name

print("Mistake 3: __init__ must be indented inside the class")


# --- Correct Pattern ---

class Dog:
    def __init__(self, name, breed="Mixed"):
        self.name = name
        self.breed = breed

    def speak(self):
        return f"{self.name} says Woof!"

print(f"\n--- Correct Pattern ---")
dog1 = Dog("Buddy", "Labrador")
dog2 = Dog("Max")                     # Uses default breed

print(dog1.speak())                    # Buddy says Woof!
print(f"{dog2.name} ({dog2.breed})")   # Max (Mixed)


# --- Key Takeaways ---
# 1. __init__ is the constructor — runs automatically on object creation
# 2. self is always the first parameter — refers to the current object
# 3. Use self.attribute = value to initialize state
# 4. Guarantees initialization — objects always start with required data
# 5. Can validate inputs, compute derived fields, set defaults
# 6. Common mistakes: forgetting self, name=name instead of self.name=name
