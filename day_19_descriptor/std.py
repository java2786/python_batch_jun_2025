class IdNumber:
    
    def __get__(self, instance, owner):
        print("Getting id")
        return instance._id
    
    def __set__(self, instance, value):
        print("setting id")
        # controll - handle logic
        if not isinstance(value, int):
            raise ValueError("This is not a number")
        elif value<0:
            raise ValueError("Number can not be negative")
    
        instance._id = value 

    def __delete__(self, instance):
        del instance._id

class Student:
    id = IdNumber()
    
    def __init__(self, name, id):
        self.name = name
        self.id = id # self.id.__set__(id)
        
std = Student("Ramesh", 25)
# del std.id
print(std.id) # std.id.__get__()
std.id = 58
print(std.id)
