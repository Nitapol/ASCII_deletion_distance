# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import multiprocessing
import numpy.ctypeslib as ctl
import ctypes
import platform


def fee(c): return ord(c)


def distance1c(a, b):  # Algorithm #5 Python calls C. (Reference): Brute force.
    a1 = a.encode('utf-8')
    b1 = b.encode('utf-8')
    return py_distance1C(ctypes.c_char_p(a1), ctypes.c_char_p(b1))

def distance8c(a, b):  # Algorithm #5 Python calls C. (Reference): Brute force.
    a1 = a.encode('utf-8')
    b1 = b.encode('utf-8')
    return py_distance8C(ctypes.c_char_p(a1), ctypes.c_char_p(b1))

def assert_1(a, b, c):
    d = distance8c(a, b)
    if d != c:
        print('*** Error:', a, b, c, '!=', d)
        exit(1)


def correct_cpu(cpu_time):
    pv1, pv2, _ = platform.python_version_tuple()
    pcv = platform.python_compiler()
    if pv1 == '3' and '5' <= pv2 <= '8' and pcv == 'Clang 6.0 (clang-600.0.57)':
        cpu_time /= 2.0
    return cpu_time


# def distance1(a, b):  # Algorithm #1 (Reference): Brute force.
#     if a == b:
#         return 0
#     d = sys.maxsize
#     for i, c in enumerate(a):
#         d = min(d, fee(c) + distance1(a[:i]+a[i+1:], b))
#     for i, c in enumerate(b):
#         d = min(d, fee(c) + distance1(a, b[:i]+b[i+1:]))
#     return d


def worker(n0, n1):
    t = time.process_time()
    dt = 0
    while n0 < n1:
        s = "{0:05d}".format(n0)
        for j in range(6):
            e = s[:j]
            f = s[j:]
            de = distance8c(e, f)
            df = distance8c(f, e)
            dt += de
            assert(de == df)
        n0 += 1
    n0 = n0 * 12
    t = time.process_time() - t
    print(("%f") % (t))
    return t, dt


if __name__ == "__main__":
    print('Python version  :', platform.python_version())
    print('       build    :', platform.python_build())
    print('       compiler :', platform.python_compiler())
    lib = ctl.load_library('distance1C.so', './')
    py_distance1C = lib.distance1C
    py_distance1C.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    py_distance8C = lib.distance8C
    py_distance8C.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    W = 4
    N = 100000
    M = N // W
    assert distance1c("cool", "cold") == fee('o') + fee('d')
    assert distance1c("!~!", "~!!") == 2 * fee('!')  # ! vs ~ (33 vs 126)

    start = time.perf_counter()
    procs = []
    pool = multiprocessing.Pool(processes=W)
    for n in range(W):
        proc = pool.apply_async(worker, args=(n * M, (n + 1) * M))
        procs.append(proc)

    dt = 0
    tt = 0
    for proc in procs:
        t, d = proc.get();
        tt += t
        dt += d
    t = time.perf_counter() - start
    n = N * 12
    print(("%f,%d,%d,%f,%f") % (t, dt, n, t/n,tt/t), sep=',')
