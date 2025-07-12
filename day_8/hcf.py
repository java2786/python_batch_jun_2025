a = 24
b = 16

# 10, 4 = 24%10
# 4, 2=10%4
# 2, 0=4%2

x, y = a, b 

while y!=0:
    x, y = y, x%y

print(f"HCF of {a} and {b} is {x}")

if x==1:
    print(f"{a} and {b} are co-prime")