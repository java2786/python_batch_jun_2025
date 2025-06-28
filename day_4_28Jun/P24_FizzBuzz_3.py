def fizzbuzzgame(n):
    result = [] 
    # [1,2,"Fizz", 4, "Buzz"]

    for i in range(0, n):
        num = i+1
        if(num%3==0 and num%5==0):
            result.append("FizzBuzz")
        elif num % 3 ==0:
            result.append("Fizz")
        elif num%5==0:
            result.append("Buzz")
        else:
            # result.append(f"{num}")
            result.append(str(num))
            
        

    return result

output = fizzbuzzgame(6) # [1,2, "Fizz", 4, "Buzz", "Fizz"]
print(output)

