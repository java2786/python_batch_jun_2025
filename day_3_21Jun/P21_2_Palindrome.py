num = int(input("Enter a number: "))
copy = num
result = 0

while num>0:
    lastDigit = num%10
    result = (result * 10) + lastDigit
    num = num // 10

print(f"Reverse of {copy} is {result}")

# original number and reverse numbers are same, if yes num is palindrome

# 121
# 12321
# madam
# mam
# nitin 
# racecar

# kanak