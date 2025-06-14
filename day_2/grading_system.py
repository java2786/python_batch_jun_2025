std_name = "Ramesh"
std_marks = 56

# 85 -> Grade A, 60 -> Grade B, 40 -> Grade C, else -> Grade D
if std_marks > 84:
    print("Grade A")
else:
    if std_marks >= 60:
        print("Grade B")
    else:
        if std_marks >= 40:
            print("Grade C")
        else:
            print("Grade D")