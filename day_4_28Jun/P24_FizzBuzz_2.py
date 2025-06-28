result = [] 
# [1,2,"Fizz", 4, "Buzz"]

n = 5

for i in range(0, n):
    num = i+1
    if(num%3==0 and num%5==0):
        result.append("FizzBuzz")
    elif num % 3 ==0:
        result.append("Fizz")
    elif num%5==0:
        result.append("Buzz")
    else:
        result.append(num)
    

print(result)