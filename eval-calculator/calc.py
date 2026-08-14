import sys
from math import *

FLAG = open("flag.txt").read().strip()

try:
    print(repr(eval(sys.stdin.read(), locals())))
except Exception as ex:
    print(f"{type(ex).__name__}: {ex}")
