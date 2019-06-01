# Better Performance and Corner cases:
# 1. multiples of 1?
# 2. calculate nCr quickly and efficiently
# 3. input 2, 4, 6, not coprimes, OK?
# 4.
from math import factorial

# see this link here:

# description:
# If we list all the natural numbers below 10 that are multiples of 3 or 5,
# we get 3, 5, 6 and 9. The sum of these multiples is 23.
#
# Find the sum of all the multiples of 3 or 5 below 1000.


# this function returns the sum of all the multiples of 3 or 5 below integer n:
# note: since it is below n, you should pass n - 1 as the parameters to the multiple function

def multiple(n):
    threeNumbers = n // 3
    fiveNumbers = n // 5
    fifteenNumbers = n // 15

    threeSum = (3 + (n - n % 3)) * threeNumbers / 2
    fiveSum = (5 + (n - n % 5)) * fiveNumbers / 2
    fifteenSum = (15 + (n - n % 15)) * fifteenNumbers / 2

    totalSum = threeSum + fiveSum - fifteenSum
    return totalSum


# first augmented version of multiple, so that it can handle multiples of any sets of numbers,
# in which any two numbers in this set are coprime.
# see what coprime means: [In number theory, two integers a and b are said to be
# relatively prime, mutually prime, or coprime (also written co-prime)
# if the only positive integer (factor) that divides both of them is 1.]
# why I choose to make them coprime: seems to me that this is easy to code, I don't
# wanna deal with cases such as multiples of 2, 4, 6 in this Augmented 1 version.
# In this Augmented 1 version, I wanna deal with cases such as 2, 3, 5, --- 7. In the future version,
# I might deal with the case that the multiples are not coprimes.

# this multipleA1 takes in the same meaning n as multiple(), and another list of integers
# containing the multiples that are dealt with. example call: [multipleA1(10, [2, 3, 5])

def multipleA1(n, lst):

    length = len(lst)
    # store the times of each multiples in a new list
    listSingle = [n // x for x in listBuildingSorted(lst, n)]
    print(listSingle)
    print(listBuildingSorted(lst, n))

    # store the sums of each multiples in a new list
    time = 0
    listSum = []
    while time != len(listSingle):
        listSum += [calcSum(listBuildingSorted(lst, n)[time], n, listSingle[time])]
        time += 1

    print(listSum)

    i = 1
    time = 0
    totalSum = 0
    while time < len(listSum):
        j = 1
        if i % 2 == 1:
            while j <= nCr(length, i) and time < len(listSum):
                totalSum += listSum[time]
                j += 1
                time += 1
        else:
            while j <= nCr(length, i) and time < len(listSum):
                totalSum -= listSum[time]
                j += 1
                time += 1
        i += 1
    return totalSum

# takes in a list, such as [2, 3, 5] and return [2, 3, 5] + [2 * 3, 2 * 5, 3 * 5] + [2 * 3 * 5]
# note: this function cannot return the order I specified above(sorted order?), so I have to sort it.
# Don't know how to get this [2, 3, 5, 6, 10, 15, 30] directly, using the combinations and/or permutations library
# might be a solution

def listBuilding(lst):
    length = len(lst)
    if len(lst) == 2:
        return [lst[0], lst[1], lst[0] * lst[1]]
    else:
        previous = listBuilding(lst[:(length - 1)])
        return previous + [lst[length - 1]] + [(lst[length - 1] * x) for x in previous]


# this function takes in an unsorted array and returns the sorted version and is less than or equal to n
# by just calling the built-in python sorting function
def listBuildingSorted(lst, n):
    return [_ for _ in sorted(listBuilding(lst)) if _ <= n]

# this function do the thing exactly the same as this code in the multiple(n) method
# [code: threeSum = (3 + (n - n % 3)) * threeNumbers / 2]

def calcSum(x, n, t):
    return (x + (n - n % x)) * t / 2


# this function computes the value of C(i, n), and store the results in an int[] array
# for example: C(i, 3) should return [C(0, 3), C(1, 3), C(2, 3), C(3, 3)]
# I used a stupid idea here: comb = list(combinations([2, 1, 3], 2)),
# I can get the length by actually calling len() on comb
def CFunction(n):
    return [nCr(n, r) for r in range(n+1)]

# this function is a "private helper" function of CFunction, which computes exactly (n chooses r)
def nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n-r))

# Main Function
if __name__ == '__main__':
    # print("you should pass in n-1 if you want to compute the sum below n")
    # print("sum of multiples of 3 or 5 below 1000 is:", multiple(999))


    # print(listBuilding([2, 3, 5]))
    # print(listBuildingSorted([2, 3, 5]))


    array = []
    print("你的 multiples 是? ")
    print("示例，请输入 2 3 5， 用空格隔开")
    inputList = input("请输入你的 multiples, 并用空格隔开: ")
    inputList = inputList.split()
    for i in inputList:
        array.append(int(i))
    print("你刚才输入的列表为: ", array)
    inputLimit = int(input("请输入你想要计算的极限值: (包含) "))
    print("你刚才输入的极限值为: ", inputLimit)
    print("multiples of", array, "的和小于等于", inputLimit, "是: ", multipleA1(inputLimit, array))

    # print(CFunction(5))