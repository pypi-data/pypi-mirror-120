![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)


# PTTHREADS
> Library for easy threading

## Installation
```
pip install ptthreads
```

## How to use
import ptthreads into your script, and call it's functions.

## Usage examples
```python
# Example of process items from list
from ptthreads import ptthreads

def my_function(item):
    print(item)
    return item

my_list  = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
threads = 20
thread_obj = ptthreads.ptthreads()
result = thread_obj.threads(my_list, my_function, threads)
print(result)
```

```python
# Example of process items from text file
from ptthreads import ptthreads

def my_function(item):
    print(item)
    return item

threads = 20 
thread_obj = ptthreads.ptthreads()
try:
    with open("dict.txt", "r") as f:
        items = [i.strip() for i in f.readlines()]
        result = thread_obj.threads(items, my_function, threads)
        print(result)
except Exception as e:
    exit(e)
```

## Printlock
To avoid overlapping prints between threads, save output to printlock

```python
# Example of printlock
from ptthreads import ptthreads

def my_function(item):
    printlock = ptthreads.printlock()
    printlock.add_string_to_output(item)
    printlock.add_string_to_output("Some text")
    printlock.add_string_to_output("Some more text")
    printlock.lock_print_output()
    return item

my_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
threads = 20
thread_obj = ptthreads.ptthreads()
result = thread_obj.threads(my_list, my_function, threads)
```

## Version History

* 0.0.1
    * Alpha release

## License

Copyright (c) 2020 HACKER Consulting s.r.o.

ptthreads is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ptthreads is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ptthreads.  If not, see <https://www.gnu.org/licenses/>.