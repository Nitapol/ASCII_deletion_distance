# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import numpy.ctypeslib as ctl
import ctypes
import platform


def fee(c): return ord(c)


def distance1c(a, b):  # Algorithm #5 Python calls C. (Reference): Brute force.
    a1 = a.encode('utf-8')
    b1 = b.encode('utf-8')
    return py_distance1C(ctypes.c_char_p(a1), ctypes.c_char_p(b1))


def distance8c(a, b):
    a1 = a.encode('utf-8')
    b1 = b.encode('utf-8')
    return py_distance8C(ctypes.c_char_p(a1), ctypes.c_char_p(b1))


def assert_1(a, b, c):
    d = distance1c(a, b)
    if d != c:
        print('*** Error:', a, b, c, '!=', d)
        exit(1)


def correct_cpu(cpu_time):
    pv1, pv2, _ = platform.python_version_tuple()
    pcv = platform.python_compiler()
    if pv1 == '3' and '5' <= pv2 <= '8' and pcv == 'Clang 6.0 (clang-600.0.57)':
        cpu_time /= 2.0
    return cpu_time


def test(func1, func2, name):
    t = time.perf_counter()
    c = time.process_time()
    n = 0
    dt = 0
    while n < 100000:
        s = "{0:05d}".format(n)
        for j in range(6):
            e = s[:j]
            f = s[j:]
            de = func1(e, f)
            df = func2(f, e)
            dt += de
            assert(de == df)
        n += 1
    n = n * 12
    t = time.perf_counter() - t
    c = correct_cpu(time.process_time() - c)
    print(t, dt, n, t/n, c, name, sep=',')


if __name__ == '__main__':
    print('Python version  :', platform.python_version())
    print('       build    :', platform.python_build())
    print('       compiler :', platform.python_compiler())
    lib = ctl.load_library('distance1C.so', './')
    py_distance1C = lib.distance1C
    py_distance1C.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    py_distance8C = lib.distance8C
    py_distance8C.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    assert_1("at", "cat", fee('c'))
    assert_1("cool", "coal", fee('a') + fee('o'))
    assert_1("cool", "cold", fee('o') + fee('d'))
    assert_1("!~!", "~!!", 2 * fee('!'))  # ! vs ~ (33 vs 126)
    test(distance8c, distance8c, "distance1C")
