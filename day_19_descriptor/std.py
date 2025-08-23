# class IdNumber:
#     def __get__(self, instance, owner):
#         print("Getting id")
#         return instance.id
    
#     def __set__(self, instance, value):
#         print("setting id")
#         # controll - handle logic
#         if not isinstance(value, int):
#             raise ValueError("This is not a number")
#         instance.id = value 

#     def __delete__(self, instance):
#         del instance.id

# class Student:
#     id = IdNumber()
    
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id 
        
# std = Student("Ramesh", 25)
# del std