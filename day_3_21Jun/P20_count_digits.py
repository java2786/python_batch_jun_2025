num = int(input("Enter a number: "))

# # for 1 digit
# if num > -10 and num<10:
#     print("Single digit")
# elif num>9 and num<100:
#     print("2 digits")
# elif num<-9 and num>-100:
#     print("2 digits")
    
# print(num/10)
# print(num//10)
# print(num%10)
# n = 0

count = 0
copy = num

while num>0:
    count = count + 1
    num = num//10
    
print(f"Total digits in {copy} are {count}")