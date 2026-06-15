# while condition:
#   statement

# print all numbers till 5
count = 1
while count <= 5:
    print(count)
    count += 1 # count = count + 1

# print all odd numbers till 10 
# this is running 5 times 
count = 1
while count <= 10:
    print(count)
    count += 2

# this is running 10 times 
count = 1
while count <= 10:
    if count % 2 == 0:
        print(count)
    count += 1 