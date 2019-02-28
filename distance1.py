# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import platform
import sys


def penalty(char): return ord(char)


def distance1(str1, str2):  # Algorithm #1 (Reference): Brute force.
    if str1 == str2:
        return 0
    score = sys.maxsize  # Enough for the worst sum of 8421504 bytes in 32bit.
    for j, c in enumerate(str1):
        score = min(score, penalty(c) + distance1(str1[:j]+str1[j+1:], str2))
    for j, c in enumerate(str2):
        score = min(score, penalty(c) + distance1(str1, str2[:j]+str2[j+1:]))
    return score


if __name__ == '__main__':
    print(platform.node())
    (mac_ver, _, _) = platform.mac_ver()
    if mac_ver is not None and mac_ver != "":
        print("macOS version", mac_ver)
    print(platform.platform())
    print("Python", platform.python_build(), platform.python_compiler())
    print("Executing in", "64bit" if sys.maxsize > 2 ** 32 else "32bit")

    assert(distance1("at", "cat") == penalty('c'))
    assert(distance1("bat", "cat") == penalty('b') + penalty('c'))
    assert(distance1("!~!", "~!!")) == 2 * penalty('!')  # ! vs ~ (33 vs 126)
    assert(distance1("!!~", "!~!")) == 2 * penalty('!')  #
    t = time.process_time()
    n = 0
    N = 0
    total_score = 0
    while n <= 99999:
        s = "{0:05d}".format(n)
        for i in range(len(s) + 1):
            s1 = s[:i]
            s2 = s[i:]
            score1 = distance1(s2, s1)
            score2 = distance1(s1, s2)
            N += 2
            total_score += score1
            assert(score1 == score2)
        n += 1
    t = time.process_time() - t
    print(t, total_score, N, t/N, sep=',')
