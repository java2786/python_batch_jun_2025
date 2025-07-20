# write into a file
filename = "comic.txt"

with open(filename, 'a') as file_write_object:
    file_write_object.write("ABC.\n")

# read from a file
with open(filename) as file_read_object:
    lines = file_read_object.readlines()
    
# print(type(lines))
# for line in lines:
#     print(line)
for i in range(0, len(lines)):
    print(f"{i+1} => {lines[i]}", end="")