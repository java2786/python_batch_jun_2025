import json 

with open("./records.json", "r") as file:
    data = json.load(file)
    
print(data)