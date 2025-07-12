a = 6
b = 4

lcm = max(a,b)
while True:
    if(lcm%a==0 and lcm%b==0):
        break
    lcm = lcm+1
    
print(f"LCM of {a} and {b} is {lcm}")
