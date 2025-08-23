""" 
Public = accessible everywhere

Protected = intended for class and child class

Private = within the class (no access outside the class)
"""

class Train:
    def __init__(self, name, number):
        self.name = name        # public
        self.number = number    # public
    
    def show_details(self):
        print(f"Train: {self.name}, Number: {self.number}")
        

# print(name)
# print(self.name)
rajdhani = Train("Rajdhani Express", 12312)
print("Name",rajdhani.name)
print("Number",rajdhani.number)
rajdhani.show_details()

