# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import platform
import sys


def fee(char): return ord(char)

# Loop 999 total 1332108
# 6.63 1+1
# 5.18 1+2
# 5.98 1+3
# 3.50 1+4
# 3.47 1+5
# Loop 99999 total 139880640
#   9.37 5+5
#   7.61 4+4
# 509.67 3+3
# 408.19 2+2
# 675.63 1+1

def distance1(a, b):  # Algorithm #1 (Reference): Brute force.
    if a == b:
        return 0
    score = sys.maxsize  # Enough for the sum of 3.62e+7 Gigabytes in 64bit.
    for j, c in enumerate(a):
        score = min(score, fee(c) + distance1(a[:j]+a[j+1:], b))
    for j, c in enumerate(b):
        score = min(score, fee(c) + distance1(a, b[:j]+b[j+1:]))
    return score

# Algorithm #2: Remove char and call the recursion only if length >=


def distance2(r1, r2):
    l1 = len(r1)
    l2 = len(r2)
    if l1 == l2 and (l1 == 0 or r1 == r2):
        return 0
    d = sys.maxsize
    l1 -= 1
    l2 -= 1
    if l1 >= l2:
        j = 0
        while True:
            d = min(d, fee(r1[j]) + distance2(r1[:j]+r1[j+1:], r2))
            if j == l1:
                break
            j += 1
    if l2 >= l1:
        j = 0
        while True:
            d = min(d, fee(r2[j]) + distance2(r1, r2[:j]+r2[j+1:]))
            if j == l2:
                break
            j += 1
    return d

# Algorithm #3: stop the recursion if not possible to improve the best score. ##


def distance3_(t1, t2, current, best):
    if t1 == t2:
        return current
    for i1, c1 in enumerate(t1):
        n1 = fee(c1) + current
        if n1 < best:
            best = min(best, distance3_(t1[:i1] + t1[i1+1:], t2, n1, best))
    for i2, c2 in enumerate(t2):
        n2 = fee(c2) + current
        if n2 < best:
            best = min(best, distance3_(t1, t2[:i2] + t2[i2+1:], n2, best))
    return best


def distance3(t1, t2):
#    ''   '00000'
    return distance3_(t1, t2, 0, sys.maxsize)

# Algorithm #4: Delete unique (only present in one) characters from each string.
#               Plus $3.


def distance4_(string1, string2, current, best):
    if string1 == string2:
        return current
    set1 = set(string1)
    set2 = set(string2)
    intersection = set1 & set2
    string = ""
    for c in string1:
        if intersection.issuperset(c):
            string += c
        else:
            current += fee(c)
    string1 = string
    string = ""
    for c in string2:
        if intersection.issuperset(c):
            string += c
        else:
            current += fee(c)
    string2 = string
    if string1 == string2:
        return current
    for i1, c1 in enumerate(string1):
        n1 = fee(c1) + current
        if n1 < best:
            best = min(best, distance4_(
                string1[:i1] + string1[i1+1:], string2, n1, best))
    for i2, c2 in enumerate(string2):
        n2 = fee(c2) + current
        if n2 < best:
            best = min(best, distance4_(
                string1, string2[:i2] + string2[i2+1:], n2, best))
    return best


def distance4(string1, string2):
    return distance4_(string1, string2, 0, sys.maxsize)


# Algorithm #5: Remove leading and trailing the same characters. Plus $4.

def distance5_(string1, string2, current, best):
    if string1 == string2:
        return current
    while len(string1) > 0 and len(string2) > 0 and string1[0] == string2[0]:
        string1 = string1[1:]
        string2 = string2[1:]
    while len(string1) > 0 and len(string2) > 0 and string1[-1] == string2[-1]:
        string1 = string1[:-1]
        string2 = string2[:-1]
    intersection = set(string1) & set(string2)

    def remove_unique(inp):
        out = ""
        for c in inp:
            if intersection.issuperset(c):
                out += c
            else:
                nonlocal current
                current += fee(c)
        return out
    string1 = remove_unique(string1)
    string2 = remove_unique(string2)
    if string1 == string2:
        return current
    for i1, c1 in enumerate(string1):
        n1 = fee(c1) + current
        if n1 < best:
            best = min(best, distance5_(
                string1[:i1] + string1[i1+1:], string2, n1, best))
    for i2, c2 in enumerate(string2):
        n2 = fee(c2) + current
        if n2 < best:
            best = min(best, distance5_(
                string1, string2[:i2] + string2[i2+1:], n2, best))
    return best


def distance5(string1, string2):
    return distance5_(string1, string2, 0, sys.maxsize)


if __name__ == '__main__':
    assert(distance1("at", "cat") == fee('c'))
    exit(1)

    print(platform.node())
    (mac_ver, _, _) = platform.mac_ver()
    if mac_ver is not None and mac_ver != "":
        print("macOS version", mac_ver)
    print(platform.platform())
    print("Python", platform.python_build(), platform.python_compiler())
    print("Executing in", "64bit" if sys.maxsize > 2 ** 32 else "32bit")

    assert(distance1("at", "cat") == fee('c'))
    assert(distance1("bat", "cat") == fee('b') + fee('c'))
    assert(distance1("!~!", "~!!")) == 2 * fee('!')  # ! vs ~ (33 vs 126)
    assert(distance1("!!~", "!~!")) == 2 * fee('!')  #

    t = time.process_time()
    n = 0
    N = 0
    total_score = 0
    while n <= 99999:
        s = "{0:05d}".format(n)
        for i in range(len(s) + 1):
            s1 = s[:i]
            s2 = s[i:]
            score1 = distance5(s2, s1)
            score2 = distance5(s1, s2)
            N += 2
            total_score += score1
            if score1 != score2:
                print(score1, " ", score2, " '", s1, "', '", s2, "' ",
                      ord('0'), sep='')
            assert(score1 == score2)
        n += 1
    t = time.process_time() - t
    print(t, total_score, N, t/N, sep=',')
