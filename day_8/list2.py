# Create a list of n elements and swap first and last.
list = [4,5,2,3,4,1]

print("Original list",list)

print("Before swap A:",list[0],",B:",list[len(list)-1])
# c = list[0]
# list[0] = list[len(list)-1]
# list[len(list)-1] = c
# print("After swap A:",list[0],",B:",list[len(list)-1])

# list[0], list[len(list)-1] = list[len(list)-1], list[0]

# print("Last element:,",list[-1])
list[0], list[-1] = list[-1], list[0]
print("List is", list)