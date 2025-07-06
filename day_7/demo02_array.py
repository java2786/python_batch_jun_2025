import array 

int_array = array.array("i")

print(type(int_array))

for i in range(1, 6):
    int_array.append(i)

# int_array.append("Arun")
print(int_array)


vowels_array = array.array("u", ['a', 'e', 'i'])
vowels_array.append('o')
vowels_array.append('u')
print(vowels_array)

print(len(vowels_array))


