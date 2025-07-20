class Student():
    def __init__(self, name, a):
        self.name = name 
        if a>0:
            self.age = a 
        else:
            self.age = 20
        print("Student object created")
        
        
std = Student("Ramesh", 21)
std2 = Student("Mukesh", -19)

print(type(std))
print(f"Student's name is {std.name} and {std.age} years old.")
print(f"Student's name is {std2.name} and {std2.age} years old.")