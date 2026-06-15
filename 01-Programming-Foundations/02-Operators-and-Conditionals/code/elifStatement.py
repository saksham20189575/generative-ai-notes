score = 60
# First match wins — rest skipped
if score >= 90: 
    grade = "A"
elif score >= 80: 
    grade = "B"  
elif score >= 70: 
    grade = "C"
else:            
    grade = "F" # runs!

# grade is "F" — correct!
print(grade)