std_name = input("Enter student's name: ")
std_marks = int(input("Enter student's marks: "))
grade = ""
# 85 -> Grade A, 60 -> Grade B, 40 -> Grade C, else -> Grade D
if std_marks > 84:
    grade = "Grade A"
elif std_marks >= 60:
    grade = "Grade B"
elif std_marks >= 40:
    grade = "Grade C"
else:
    grade = "Grade D"
    
print(f"{std_name} has scored {std_marks} marks and final grade is {grade}")