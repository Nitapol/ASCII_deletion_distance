# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import sys


def fee(c): return ord(c)


def distance1(a, b):  # Algorithm #1 (Reference): Brute force.
    if a == b:  # success, if strings are equal
        return 0
    d = sys.maxsize  # Enough for the worst sum of 8421504 bytes in 32bit.
    for i, c in enumerate(a):  # for each index and character in  a
        d = min(d, fee(c) + distance1(a[:i]+a[i+1:], b))
    for i, c in enumerate(b):
        d = min(d, fee(c) + distance1(a, b[:i]+b[i+1:]))
    return d  # minimal achieved distance for a & b strings


if __name__ == '__main__':
    assert distance1("cool", "cold") == fee('o') + fee('d')
    assert distance1("!~!", "~!!") == 2 * fee('!')  # ! vs ~ (33 vs 126)
    t = time.process_time()
    n = 0  # cycle number
    dt = 0  # distance total sum
    while n < 100000:
        s = "{0:05d}".format(n)  # 00000, 00001, 00002, ..., 99999
        for j in range(6):
            e = s[:j]  # "", "0", "00", "000", "0000", "00000" ...
            f = s[j:]  # "00000", "0000", "000", "00", "0", "" ...
            de = distance1(e, f)
            df = distance1(f, e)
            dt += de
            assert(de == df)
        n += 1
    n = n * 12  # now it is number of distance1 calls
    t = time.process_time() - t
    print(t, dt, n, t/n, sep=',')
