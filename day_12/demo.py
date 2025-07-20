nums = [4,6,7,2,5,3]
nums.sort()
# output => 4 is missing number

print(nums)
flag = True
for i in range(0, len(nums)):
    count = i+1
    if(nums[i]!=count):
        print(f"{count} is missing number")
        flag = False   
        break

if flag:
    print(f"{len(nums)+1} is missing number")