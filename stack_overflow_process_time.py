import time
import sys
import platform


def distance(a, b):
    if a == b:
        return 0
    d = sys.maxsize
    for i, c in enumerate(a):
        d = min(d, ord(c) + distance(a[:i]+a[i+1:], b))
    for i, c in enumerate(b):
        d = min(d, ord(c) + distance(a, b[:i]+b[i+1:]))
    return d


print("Python", platform.python_build(), platform.python_compiler())
cpu = time.process_time()
clock = time.perf_counter()
d = distance("12345", "abcde")
clock = time.perf_counter() - clock
cpu = time.process_time() - cpu
print("CPU Time:", cpu, "Wall Clock:", clock, " Distance:", d)
