# School -> 3 students -> name, age, address, email

# Show all student details of school
# Show nth student details from the school
# Assign nth student details -> name, age, address, email

class Student:
    def show_student(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}, Email: {self.email}")
        
    def __init__(self, name, age, address, email):
        self.name = name
        self.age = age 
        self.address = address 
        self.email = email 
        

class School:
    def __init__(self):
        self.students = []
        
        self.students.append(Student("Ramesh", 23, "Ghaziabad", "ram@gmail.com"))
        self.students.append(Student("Rajesh", 19, "Nodia", "rajesh@gmail.com"))
        self.students.append(Student("Mukesh", 28, "Duhai", "mukesh@gmail.com"))
    
    def show_all_students(self):
        for std in self.students:
            std.show_student()
        print("\n")
    
    def show_nth_student(self, index):
        if ((index < 0) or (index >= len(self.students))):
            print("invalid index, boundary error")
            return
        else:
            std = self.students[index]
            std.show_student()
            
    def student_enrollment(self, index, name, age, address, email):
        if ((index < 0) or (index >= len(self.students))):
            print("invalid index, boundary error")
            return
        else:
            std = self.students[index]
            print("Student type",type(std))
            std.name = name 
            std.age = age 
            std.address = address
            std.email = email 


driving_school = School()
driving_school.show_all_students()
driving_school.show_nth_student(2)
driving_school.student_enrollment(1, "Ganesh", 24, "Pune", "ganesh@ymail.com")
driving_school.show_all_students()


# fruits = []
# fruits.append("mango")
# fruits.append("grapes")
# fruits.append("apple")

# print(fruits)
# print(fruits[1])
# fruits[1] = "guava"
# print(fruits)

