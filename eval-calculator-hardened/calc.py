import sys, math

try:
    print(repr(eval(sys.stdin.read(), math.__dict__)))
except Exception as ex:
    print(f"{type(ex).__name__}: {ex}")
