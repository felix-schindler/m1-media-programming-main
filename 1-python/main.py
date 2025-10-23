import math


# functions
def add(a: int, b: int) -> int:
    return a + b


# call function
print(add(1, 2))

# lists / arrays
list = [42, 66, -4, "felix"]
list.append(add(123, 456))
print(list)

# strings
str = "felix"
print(str.lower().count("x"))

# read cmd line
your_name = input("Please enter your name: ")
print("You're called", your_name)

# use packages
print(math.sqrt(9))

# read text file `with`
with open("file.txt") as f:
    print(f.read())
