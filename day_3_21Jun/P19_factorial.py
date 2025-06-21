# n = 5
# fact = 5 * 4 * 3 * 2 * 1 = 120

# n = 3
# fact = 3 * 2 * 1 = 6

# n = 1 
# fact = 1

# n = 0
# fact = 1

n = int(input("Enter a number: "))

if n < 0:
    print("Factorial of a negative num is not defined")
elif n==0:
    print("Factorial of 0 is 1")
else:
    fact = 1
    for i in range(0, n):
        fact = fact * (i+1)
    
    print(f"{n}! = {fact}")