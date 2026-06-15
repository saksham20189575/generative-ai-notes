age_str = input("Age: ") # input will be in string 
age = int(age_str) # string to int

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
