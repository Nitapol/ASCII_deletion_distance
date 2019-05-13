# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import sys
import multiprocessing
from distance3 import  distance8, distance9, correct_cpu


def fee(c): return ord(c)


def distance1(a, b):  # Algorithm #1 (Reference): Brute force.
    if a == b:
        return 0
    d = sys.maxsize
    for i, c in enumerate(a):
        d = min(d, fee(c) + distance1(a[:i]+a[i+1:], b))
    for i, c in enumerate(b):
        d = min(d, fee(c) + distance1(a, b[:i]+b[i+1:]))
    return d

def worker(n0, n1):
    t = time.process_time()
    dt = 0
    while n0 < n1:
        s = "{0:05d}".format(n0)
        for j in range(6):
            e = s[:j]
            f = s[j:]
            de = distance1(e, f)
            df = distance1(f, e)
            dt += de
            assert(de == df)
        n0 += 1
    n0 = n0 * 12
    t = correct_cpu(time.process_time() - t)
    print(("%f") % (t))
    return t, dt


if __name__ == "__main__":
    W = 4
    N = 100000
    M = N // W
    assert distance1("cool", "cold") == fee('o') + fee('d')
    assert distance1("!~!", "~!!") == 2 * fee('!')  # ! vs ~ (33 vs 126)

    clock = time.perf_counter()
    cpu0 = time.process_time()
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
    cpu = time.process_time()
    clock = time.perf_counter() - clock
    cpu -= cpu0
    n = N * 12
    print(clock, dt, n, clock/n, correct_cpu(cpu), tt/W)
