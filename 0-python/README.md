Getting started with Python because I have **zero** experience.

# Takeaways

## Great namespaces

```py
c = (f - 32) / 1.8
round(c, 2)              # no math.
math.sqrt()              # here you need math.
datetime.datetime.now()  # "datetime"*2
```

## Great function names

```py
str.startswith("abc")    # no snake case
str.islower()
counter.most_common()    # snake case
```

## Synchronos IO

with open(os.path.join(os.path.dirname(__file__), "file.txt")) as f:
    print(f.read())

## Types

```py
add = lambda x, y: x * y

from typing import Callable
func: Callable[[int, int], int] = lambda x, y: x * y
```

## Dependency management

Braucht keinen Kommentar. Zum Glück gibt es inzwischen zwanzig verschiedene Methoden wovon sich jeder seinen Liebling raussucht, den aber niemand sonst benutzt.
