flag = True
a = None 
b = None 
while(flag):
    try:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        flag = False 
    except ValueError:
        print("Please try again with a number")

print(f"{a} + {b} = {a+b}")
print(f"{a} * {b} = {a*b}")