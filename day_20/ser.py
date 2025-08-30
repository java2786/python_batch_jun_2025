import json

data = {
    "name": "Ramesh",
    "city": "Pune",
    "age": "32",
    "email": "ram@gmail.com",
    "subjects": ["math", "python", "html"]
} 

# serialize -> write in file
with open("./records.json", "w") as file:
    json.dump(data, file)

# deserialize -> read from file

