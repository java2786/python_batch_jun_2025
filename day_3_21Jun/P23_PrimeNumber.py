num = int(input("Enter a number: "))

if num < 2:
    print(f"{num} is not prime number")
else:
    is_prime = True
    for i in range(2, (num//2)+1):
        if num%i==0:
            print(f"{num} is not a prime number")
            is_prime = False
            break # exit the closest loop
    if is_prime==True: 
        print(f"{num} is prime number")