# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import sys
# a, b, e, f, s - strings
# c - character;
# i, j, n, d - integers for indices , numbers, distances


def fee(c): return ord(c)


def distance1a(a, b):  # Algorithm #1 (Reference): Brute force.
    if a == b:
        return 0
    score = sys.maxsize
    for i, c in enumerate(a):
        a.pop(i)
        score = min(score, c + distance1a(a, b))
        a.insert(i, c)
    for i, c in enumerate(b):
        b.pop(i)
        score = min(score, c + distance1a(a, b))
        b.insert(i, c)
    return score


def distance1(sa, sb):
    a = [fee(c) for c in sa]
    b = [fee(c) for c in sb]
    return distance1a(a, b)


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
