# Copyright (c) 2019 Alexander Lopatin. All rights reserved.
import time
import platform
import sys


def penalty(char): return ord(char)


def distance1(str1, str2):  # Algorithm #1 (Reference): Brute force.
    if str1 == str2:
        return 0
    score = 2147483647  # Should be enough for the worst sum of 8421504 bytes.
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

# @ iMac, Intel Core i5, 3.2 GHz
#           Time sec,total_score,calls,Time per call (sec)
#  Python 3.5: 501.1,139880640,1200000,0.000417602
#  (with score = sum([penalty(c) for c in str1 + str2]))
#              372.1,139880640,   -   ,0.000310051 (score = float('inf'))
#              344.5,    -    ,   -   ,0.000287047 (score = 2147483647)
#   dummy        2.3,157500000,   -   ,0.000001952 (no distance1() calls)
#  Python 3.7: 934.2,    -    ,   -   ,0.000778530
#  Python 2.7: 478.7,    -    ,   -   ,0.000398887
