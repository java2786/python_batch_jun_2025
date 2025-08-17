# Encapsulation = binding data into single unit

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age 
        
    def intro(self):
        print(f"Hello, I am {self.name} and {self.age} years old.")
        
std = Student("Ramesh", 21)
std.intro()