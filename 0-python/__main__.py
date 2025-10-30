from math import sqrt
import os


# functions
def add(a: int, b: int = 1) -> int:
    return a + b


# call function
print(add(1, 2))

# default value
print(add(123))

# lists / arrays
_list = [42, 66, -4, "felix"]
_list.append(add(123, 456))
print(_list)

# strings
str = "felix"
print(str.lower().count("x"))

# read cmd line
# your_name = input("Please enter your name: ")
your_name = "skipped"
print("You're", your_name)

# use packages
print(sqrt(9))

# read text file `with`
with open(os.path.join(os.path.dirname(__file__), "file.txt")) as f:
    print(f.read())

print(type(6.45))

# rounding
f = 100
c = (f - 32) / 1.8
print(round(c, 2))

# lamda
multiply = lambda x, y: x * y
print(multiply(123, 456))

# square
squared = lambda x: x**2
print(squared(12))


# change sth global
def change_name():
    global your_name
    your_name = "Gustav"


change_name()
print("You're now called", your_name)

# popular packages
# Data science: numpy, pandas
# Machine learning: tensorflow, pytorch
# Statistik: scipy
# Web: django

import collections

colors = ["red", "blue", "green", "blue", "blue", "red"]
collections.Counter(colors).most_common()

from abcdata import abc

print(abc)

colors_str = ", ".join(colors)
print(colors_str)

# more strings
my_str = "123456789"
print(my_str * 3)
print(my_str[0], my_str[5:], my_str[7:], my_str[3:5], my_str[-2], my_str[5:-2])
print(len(my_str))

s = "Hier steht mein name\nFelix"
print(s.split())

print(colors_str.startswith("abc"))
print(colors_str.replace("e", "a"))
print(colors_str.find("e"))
print(colors_str.strip())
print(colors_str.upper())
print(max(colors_str))

# regex
import re

print(re.sub("[xyz]", "K", "abycd"))

# interpolation
age = 2025 - 1970
print(f"Hello {your_name}, you are {age}")

import datetime

today = datetime.datetime.now()
print(today)
print(f"Heute ist {today:%d %B, %Y}")

# mutable
colors.append("orange")
print(colors)
# colors_str[3] = "T"

b = (4, 8, "three")
c = [(8, 5), 9, 3, (4, 7)]


def double_values(x, y):
    return x * 2, y * 2


d, e = double_values(3, 4)
print(d, e)

# sets
s1 = {1, 2, 3}
s2 = {3, 4, 5}
s3 = s1 | s2
print(s3, s1 - s2)
s_empty = set()

# remove
colors.pop()
del colors[0]
colors.remove("red")
print(colors)

if "red" in colors:
    print("THERE IS RED")
else:
    print("No red")

colors += ["new", "colors", "soon"]
print(colors)

colors = sorted(colors)
print(colors)

colors.reverse()
print(colors)

if len(colors) > 0 and "str".islower():
    print("WOHOO")
# elif, else

print(list(range(1, 100)))
