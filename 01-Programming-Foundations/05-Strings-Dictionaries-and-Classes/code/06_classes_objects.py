# ============================================
# Classes – Define Classes & Create Objects
# ============================================


# ============================================
# Defining Classes
# ============================================

# --- Basic Class ---

class Dog:
    pass   # Empty class (placeholder)

# Create an object (instance)
my_dog = Dog()
print("my_dog:", my_dog)
print("type:", type(my_dog))


# --- Class with a Method ---

class Dog:
    def bark(self):
        print("Woof!")

    def sit(self):
        print("Dog sits down.")

my_dog = Dog()
my_dog.bark()     # Woof!
my_dog.sit()      # Dog sits down.


# --- PascalCase Naming Convention ---

# Good: PascalCase for class names
class BankAccount:
    pass

class StudentRecord:
    pass

# Bad: snake_case (that's for functions/variables)
# class bank_account:  # Don't do this


# --- self Parameter ---
# 'self' refers to the specific object calling the method

class Greeter:
    def say_hello(self):
        print("Hello! I am", self)

g1 = Greeter()
g2 = Greeter()
print()
g1.say_hello()     # Different memory address
g2.say_hello()     # Different memory address


# ============================================
# Creating Objects (Instances)
# ============================================

print("\n" + "=" * 40)
print("CREATING OBJECTS")
print("=" * 40)

# --- Each ClassName() Creates a NEW Object ---

class Dog:
    pass

dog1 = Dog()
dog2 = Dog()
print(f"\ndog1 is dog2: {dog1 is dog2}")    # False — different objects!
print(f"dog1 id: {id(dog1)}")
print(f"dog2 id: {id(dog2)}")


# --- Objects Are Independent ---

class Student:
    def __init__(self, name):
        self.name = name

alice = Student("Alice")
bob = Student("Bob")

# Changing one doesn't affect the other
alice.name = "Alicia"
print(f"\nalice.name: {alice.name}")    # Alicia
print(f"bob.name: {bob.name}")         # Bob (unchanged!)


# --- Real-World Example: Bank Account ---

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposited ${amount}. Balance: ${self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"{self.owner} withdrew ${amount}. Balance: ${self.balance}")
        else:
            print(f"Insufficient funds! {self.owner} has ${self.balance}")

    def get_balance(self):
        return self.balance

print("\n--- Bank Account ---")
alice_acct = BankAccount("Alice", 1000)
bob_acct = BankAccount("Bob", 500)

alice_acct.deposit(200)       # Alice deposited $200. Balance: $1200
bob_acct.withdraw(100)        # Bob withdrew $100. Balance: $400
bob_acct.withdraw(600)        # Insufficient funds!

# Each account tracks its own balance
print(f"\nAlice balance: ${alice_acct.get_balance()}")
print(f"Bob balance: ${bob_acct.get_balance()}")


# --- Storing Objects in Collections ---

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

products = [
    Product("Laptop", 999),
    Product("Mouse", 25),
    Product("Keyboard", 75),
]

print("\n--- Products ---")
total_value = 0
for product in products:
    print(f"  {product.name}: ${product.price}")
    total_value += product.price

print(f"Total inventory value: ${total_value}")


# --- Objects in a Dictionary ---

class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role

team = {
    'E001': Employee("Alice", "Engineer"),
    'E002': Employee("Bob", "Designer"),
    'E003': Employee("Charlie", "Manager"),
}

print("\n--- Team Directory ---")
for emp_id, emp in team.items():
    print(f"  {emp_id}: {emp.name} ({emp.role})")


# --- Key Takeaways ---
# 1. class keyword defines a class (use PascalCase)
# 2. Object = instance of a class, created with ClassName()
# 3. Each object has unique identity and independent state
# 4. self = reference to the current object in methods
# 5. Objects can be stored in lists, dicts, etc.
