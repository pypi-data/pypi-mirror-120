# Parallely - Parallel Python made simple

[![pypi](https://img.shields.io/pypi/v/parallely.svg)](https://pypi.org/project/parallely/)
[![License](https://img.shields.io/github/license/mvilstrup/parallely)](https://github.com/mvilstrup/parallely/blob/main/LICENSE)
[![wheel](https://img.shields.io/pypi/wheel/parallely.svg)](https://pypi.org/project/parallely/)
[![python](https://img.shields.io/pypi/pyversions/parallely.svg)](https://pypi.org/project/parallely/)
[![Test Suite](https://github.com/mvilstrup/parallely/workflows/Test%20Suite/badge.svg)](https://github.com/mvilstrup/parallely/actions?query=workflow%3A%22Test+Suite%22)
[![Coverage Status](https://coveralls.io/repos/github/MVilstrup/parallely/badge.svg?branch=main)](https://coveralls.io/github/MVilstrup/parallely?branch=main)
[![docs](https://readthedocs.org/projects/parallely/badge/?version=latest)](https://parallely.readthedocs.io/en/latest/?badge=latest)

## Installation
To install this library, all you have to do is write `pip install parallely`. The library is really simple with just 3 functions. However, if needed, you can find the docs at [ReadTheDocs](https://parallely.readthedocs.io/en/latest/index.html)

# Overview

Dealing with multi-threading, parallel processes, and concurrent functions can be difficult in Python. A lot of boiler plate code is needed, and it is difficult to gauge whether it actually improved performance or not. 

In some cases, it is necessary to tailor the program to utilize the underlying computational resources. In most cases, we just want to do the same thing many times with small alterations. In these scenarios `parallely` can make your life much easier. 

# Multi Threading
Due to the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) multi threading is far from as useful in Python as it is in other langauges. However, when dealing with I/O intensive applications it can still be really usefull to have multiple threads waiting for a response in parallel instead of waiting for each response sequentially, if you are confused by this, there are plenty of tutorials etc. to [help you out](https://www.google.com/search?q=why%20multi%20thread%20python)

Most of the time we just want to make a series of webrequests. In this case `parallely` removes all complexity of handling all the threads with a single decorator `threaded`. Which is easiest to explain with an example:

```python
import time
from parallely import threaded

@threaded
def thread_function(name, duration, other_arg):
    print(f"Thread {name}: starting", other_arg)
    time.sleep(duration)
    print(f"Thread {name}: finishing", other_arg)


print("Synchronous")
thread_function(1, duration=2, other_arg="hello world")
thread_function(2, duration=1, other_arg="hello world")
# NOTICE: We can use the thread_function the exact way we would expect without any overhead

print()
print("Parallel/Asynchrous")
thread_function.map(name=[1, 2], duration=[2, 1], other_arg="hello world")
# NOTICE: the constant given to 'other_arg' is repeated in all function calls
# thread_function.map([1, 2], [2, 1], "hello world") would produce a similar result
```

As can be seen, the decorated function can be used like one would expect, which makes it easiest to test the function etc. However, it allso gets a `.map()` attribute, which can be used to run the function in a parallel manner.

# Multi Processing
Working with multiple processes is one of the only ways to get around the GIL. However, this approach has [all sorts of problems on its own](https://www.google.com/search?q=problems%20when%20working%20with%20multi%20processes%20python). In many cases transferring the data between processes takes more time than the actual calculations. However, some times it can dramatically speed things up. `parallely` makes it just as easy to work with multiple processes as it does with threads. Simply use the decorator `parallel` as can be seen in the example below.

```python
from time import time
from random import randint
from parallely import parallel


@parallel
def count_in_range(size, search_minimum, search_maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a random array"""
    rand_arr = [randint(0, 10) for _ in range(int(size))] 
    return sum([search_minimum <= n <= search_maximum for n in rand_arr])

size = 1e7

print("Sequential")
start_time = time()
for _ in range(4):
    result = count_in_range(size, search_minimum=1, search_maximum=2)
    print(result, round(time() - start_time, 2), "seconds")

print()

print("Parallel")
start_time = time()
result = count_in_range.map(size=[size, size, size, size], search_minimum=1, search_maximum=2)
print(result, round(time() - start_time, 2), "seconds")
```

# Asynchronous

```python
import asyncio
import time
from random import randint
from parallely import asynced


async def echo(delay, start_time):
    await asyncio.sleep(randint(0, delay))
    print(delay, round(time.time() - start_time, 1))

@asynced
async def main(counts):
    start_time = time.time()
    print(f"started at {time.strftime('%X')}")
    
    corr = []
    for count in range(counts):
        corr.append(echo(count, start_time))
        
    await asyncio.gather(*corr)

    print(f"finished at {time.strftime('%X')}")

# The asynchronous function can now be called in a synchronous manner without awiting it
main(10)

# It can also be called in a parallel manner
main.map([5, 5])
```