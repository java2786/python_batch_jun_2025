# take n elements and store in list

n = int(input("Enter total number of elements: "))
list = []
# print(type(n))

for i in range(n):
    new_element = int(input("Enter number to insert: "))
    list.append(new_element)
    
print("Original list",list)

a = 6
b = 3

print("Before swap A:",a,",B:",b)
c = a
a = b
b = c
print("After swap A:",a,",B:",b)