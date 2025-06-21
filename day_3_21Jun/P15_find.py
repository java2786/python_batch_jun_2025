num = int(input("Enter a number: "))

if num>=100 and num<1000:
    print(f"{num} is 3-digit number")
elif num>-1000 and num<-99:
    print(f"{num} is 3-digit negative number")
else:
    print(f"{num} is not a 3-digit number")

