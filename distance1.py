# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import sys
# a, b, e, f, s - strings
# c - character;
# i, j, n, d - integers for indices , numbers, distances


def fee(c): return ord(c)


def distance1(a, b):  # Algorithm #1 (Reference): Brute force.
    if a == b:
        return 0
    d = sys.maxsize  # Enough for the worst sum of 8421504 bytes in 32bit.
    for i, c in enumerate(a):
        d = min(d, fee(c) + distance1(a[:i]+a[i+1:], b))
    for i, c in enumerate(b):
        d = min(d, fee(c) + distance1(a, b[:i]+b[i+1:]))
    return d


if __name__ == '__main__':
    assert distance1("cool", "cold") == fee('o') + fee('d')
    assert distance1("!~!", "~!!") == 2 * fee('!')  # ! vs ~ (33 vs 126)
    t = time.process_time()
    n = 0
    dt = 0
    while n < 100000:
        s = "{0:05d}".format(n)
        for j in range(6):
            e = s[:j]
            f = s[j:]
            de = distance1(e, f)
            df = distance1(f, e)
            dt += de
            assert(de == df)
        n += 1
    n = n * 12
    t = time.process_time() - t
    print(t, dt, n, t/n, sep=',')
