n = int(input("Enter a number of terms: "))
a = 0
b = 1
nt = a+b

print(a, end=" ")
print(b, end=" ")
print(nt, end=" ")

for i in range(0, n-3):
    a = b 
    b = nt 
    nt = a+b
    print(nt, end=" ")
    
    
# 7 => 0 1 1 2 3 5 8