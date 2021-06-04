# Memfractal
An esolang by Zzo38 where data is stored in a fractal structure.

The original specification is [here](https://esolangs.org/wiki/Memfractal). Here are some things to know about my implementation that aren't in the spec:
- The instruction pointer enters the program from the arrow on the left side. (>)
- There is a extra command ($) which prints the bit stored in the current cell.
- At the end of execution, the number of 1s left in the memory is printed.
- Comments can be included above or below the program, and they will be ignored.
- Comments can also be inside the program, as long as the instruction pointer doesn't hit them.

Lastly, this was written for Python 3 and may not work on earlier versions of Python.
