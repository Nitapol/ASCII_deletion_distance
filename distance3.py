import time
from itertools import *
from distance_utilities import *


# 1 ######################################################################## 1 #

def distance1(a, b, statistics=None):
    if statistics is not None:
        statistics[len(a)+len(b)] += 1
    if a == b:
        return 0
    d = sys.maxsize
    for i, c in enumerate(a):
        d = min(d, fee(c) + distance1(a[:i]+a[i+1:], b, statistics))
    for i, c in enumerate(b):
        d = min(d, fee(c) + distance1(a, b[:i]+b[i+1:], statistics))
    return d

# 2 ######################################################################## 2 #


def distance2(a, b, statistics=None):
    la = len(a)
    lb = len(b)
    if statistics is not None:
        statistics[la+lb] += 1
    if a == b:
            return 0
    d = sys.maxsize
    la -= 1
    lb -= 1
    if la >= lb:
        i = 0
        while True:
            d = min(d, fee(a[i]) + distance2(a[:i]+a[i+1:], b, statistics))
            if i == la:
                break
            i += 1
    if lb >= la:
        i = 0
        while True:
            d = min(d, fee(b[i]) + distance2(a, b[:i]+b[i+1:], statistics))
            if i == lb:
                break
            i += 1
    return d

# 3 ######################################################################## 3 #
# Algorithm #3: stop the recursion if not possible to improve the best score. ##


def distance3_(a, b, current, best, statistics=None):
    if statistics is not None:
        statistics[len(a)+len(b)] += 1
    if a == b:
        return current
    for i, c in enumerate(a):
        j = fee(c) + current
        if j < best:
            best = min(best, distance3_(a[:i]+a[i+1:], b, j, best, statistics))
    for i, c in enumerate(b):
        j = fee(c) + current
        if j < best:
            best = min(best, distance3_(a, b[:i]+b[i+1:], j, best, statistics))
    return best


def distance3(a, b, statistics=None):
    return distance3_(a, b, 0, sys.maxsize, statistics)

# 4 ######################################################################## 4 #
# Algorithm #4: Delete unique (only present in one) characters from each string.
#               Plus $2 & #3.


def intersection_a_b(a, b, current):
    set_b = set(b)
    new_a = ""
    for c in a:
        if set_b.issuperset(c):
            new_a += c
        else:
            current += fee(c)
    return new_a, current


def string_intersection(old_a, b, current):
    a, current = intersection_a_b(old_a, b, current)
    b, current = intersection_a_b(b, old_a, current)
    return a, b, current


def distance4_(a, b, current, best, statistics=None):
    if statistics is not None:
        statistics[len(a)+len(b)] += 1
    if a == b:
        return current
    a, b, current = string_intersection(a, b, current)
    if a == b:
        return current

    def try_to_delete(a0, b0):
        nonlocal best
        for i, c in enumerate(a0):
            n1 = fee(c) + current
            if n1 < best:
                best = min(best, distance4_(
                    a0[:i] + a0[i + 1:], b0, n1, best, statistics))
        return best

    if len(a) >= len(b):
        best = min(best, try_to_delete(a, b))
    if len(b) >= len(a):
        best = min(best, try_to_delete(b, a))
    return best


def distance4(a, b, statistics=None):
    return distance4_(a, b, 0, sys.maxsize, statistics)

# 5 ######################################################################## 5 #
# Algorithm #5: Remove leading and trailing the same characters. Plus $4.


def distance5_(a, b, current, best, statistics=None):
    if statistics is not None:
        statistics[len(a)+len(b)] += 1
    if a == b:
        return current
    while len(a) > 0 and len(b) > 0 and a[0] == b[0]:
        a = a[1:]
        b = b[1:]
    while len(a) > 0 and len(b) > 0 and a[-1] == b[-1]:
        a = a[:-1]
        b = b[:-1]
    for i1, c1 in enumerate(a):
        n1 = fee(c1) + current
        if n1 < best:
            best = min(best, distance5_(
                a[:i1] + a[i1+1:], b, n1, best, statistics))
    for i2, c2 in enumerate(b):
        n2 = fee(c2) + current
        if n2 < best:
            best = min(best, distance5_(
                a, b[:i2] + b[i2+1:], n2, best, statistics))
    return best


def distance5(a, b, statistics=None):
    return distance5_(a, b, 0, sys.maxsize, statistics)


# 6 ######################################################################## 6 #
# Algorithm #6: With the help dictionary


def distance6a(a, b, di, statistics=None):
    la = len(a)
    lb = len(b)
    if statistics is not None:
        statistics[la+lb] += 1
    if a == b:
            return 0
    s = a + "," + b
    if s in di:
        return di[s]
    d = sys.maxsize
    la -= 1
    lb -= 1
    if la >= lb:
        i = 0
        while True:
            d = min(d, fee(a[i]) + distance6a(a[:i]+a[i+1:], b, di, statistics))
            if i == la:
                break
            i += 1
    if lb >= la:
        i = 0
        while True:
            d = min(d, fee(b[i]) + distance6a(a, b[:i]+b[i+1:], di, statistics))
            if i == lb:
                break
            i += 1
    di[s] = d
    return d


def distance6(a, b, dictionary=None, statistics=None):
    if dictionary is None:
        dictionary = {}
    return distance6a(a, b, dictionary, statistics)

# 7 ######################################################################## 7 #
# Algorithm #7: Dynamic Programming


def distance7(s1, s2, statistics=None):
    if statistics is not None:
        statistics[0] += 1
    m = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]
    for i in range(len(s1)+1):
        for j in range(len(s2)+1):
            if i == 0:
                m[i][j] = sum([ord(c) for c in s2[:j]])
            elif j == 0:
                m[i][j] = sum([ord(c) for c in s1[:i]])
            elif s1[i-1] == s2[j-1]:
                m[i][j] = m[i-1][j-1]
            else:
                a = ord(s1[i-1])
                b = ord(s2[j-1])
                c = a + b
                m[i][j] = min(m[i-1][j-1] + c, m[i-1][j] + a, m[i][j-1] + b)
    return m[len(s1)][len(s2)]

# 8 ######################################################################## 8 #
# Algorithm #8: Dynamic Programming & Algorithm #4


def distance8(si, sj, statistics=None):
    if statistics is not None:
        statistics[0] += 1
    if si == sj:
        return 0
    # while len(si) > 0 and len(sj) > 0 and si[0] == sj[0]:
    #     si = si[1:]
    #     sj = sj[1:]
    # while len(si) > 0 and len(sj) > 0 and si[-1] == sj[-1]:
    #     si = si[:-1]
    #     sj = sj[:-1]
    # si, sj, current = string_intersection(si, sj, 0)
    # if si == sj:
    #     return current
    li = len(si)
    # if li == 0:
    #     return current + sum([fee(c)] for c in sj)
    lj = len(sj)
    # if lj == 0:
    #     return current + sum([fee(c)] for c in si)
    ai = [fee(c) for c in si]
    aj = [fee(c) for c in sj]
    a = [[0 for _ in range(lj+1)] for _ in range(li+1)]
    for i in range(li):
        a[i+1][0] = a[i][0] + ai[i]
    for j in range(lj):
        a[0][j+1] = a[0][j] + aj[j]
    for i in range(li):
        for j in range(lj):
            if ai[i] == aj[j]:
                a[i+1][j+1] = a[i][j]
            else:
                a[i+1][j+1] = min(a[i][j] + ai[i] + aj[j], a[i][j+1] + ai[i],
                                  a[i+1][j] + aj[j])
    print(li, lj, a)
    return current + a[li][lj]


# 9 ######################################################################## 9 #
# Algorithm #9: All the best #4 (plus $2 & #3 ) and #6 combined


def distance9_(a, b, di, current, best, statistics=None):
    if statistics is not None:
        statistics[len(a)+len(b)] += 1
    if a == b:
        return current
    s = a + "," + b
    if s in di:
        return di[s]
    a, b, current = string_intersection(a, b, current)
    if a == b:
        di[a + "," + b] = current
        return current
    while len(a) > 0 and len(b) > 0 and a[0] == b[0]:
        a = a[1:]
        b = b[1:]
    while len(a) > 0 and len(b) > 0 and a[-1] == b[-1]:
        a = a[:-1]
        b = b[:-1]

    def try_to_delete(a0, b0):
        nonlocal best
        for i, c in enumerate(a0):
            n1 = fee(c) + current
            if n1 < best:
                best = min(best, distance9_(
                    a0[:i] + a0[i + 1:], b0, di, n1, best, statistics))
        return best
    if len(a) >= len(b):
        best = min(best, try_to_delete(a, b))
    if len(b) >= len(a):
        best = min(best, try_to_delete(b, a))
    di[a + "," + b] = best
    return best


def distance9(a, b, dictionary=None, statistics=None):
    if dictionary is None:
        dictionary = {}
    return distance9_(a, b, dictionary, 0, sys.maxsize, statistics)

# Tests ################################################################ Tests #


def quick_tests(f):
    assert_1(f, 'A', '', 'A')
    assert_1(f, '!', '~', '!~')
    assert_1(f, '!!', '!!!', '!')
    assert_1(f, '!!!', '!!', '!')
    assert_1(f, '', 'z', 'z')
    assert_1(f, 'ooz', 'zoo', 'zz')
    assert_1(f, 'at', 'hat', 'h')
    assert_1(f, 'cat', 'rat', 'cr')
    assert_1(f, 'cool', 'cold', 'od')
    assert_1(f, '!~!', '~!!', 2*'!')  # ! vs ~ (33 vs 126)
    assert_1(f, '~!!!', '!!!~', 6 * '!')
    assert_1(f, 'AB', 'xy', 'ABxy')


def debug_test():
    a = 'AB'
    b = 'xy'
    st = [0 for _ in range(len(a)+len(b)+1)]
    dictionary = {}
    cpu0 = time.process_time_ns()
    clock0 = time.perf_counter_ns()
    distance6(a, b, dictionary, st)
    clock1 = time.perf_counter_ns()
    cpu1 = time.process_time_ns()
    d1 = sorted((5-len(key), value, key) for (key, value) in dictionary.items())
    for ld in d1:
        print(ld)
    print(len(dictionary), len(d1))
    print(st)
    print(clock1 - clock0, cpu1 - cpu0)


def strip_distance(s):
    f = 'distance'
    i = s.find(f)
    return s if i < 0 else s[0:i]+s[i+len(f):]


def test_permutation_with_repetition(f1, f2):
    name1 = strip_distance(f1.__name__)
    name2 = strip_distance(f2.__name__)
    name = name1 + " vs " + name2 if name1 != name2 else name1 + " * 2"
    i = len(name) - 4
    print('Names' + ' ' * i + 'Len Clock  CPU Clock/Calls CPU/Calls '
          + 'Calls   Call statistics by depth:')
    for combined_string_length in range(5, 9):
        statistics1 = [0 for _ in range(combined_string_length+1)]
        statistics2 = [0 for _ in range(combined_string_length+1)]
        products = product('!0Az~', repeat=combined_string_length)
        cpu = time.process_time()
        clock = time.perf_counter()
        for p in list(products):
            string = ''.join(p)
            for index in range(len(string) + 1):
                a = string[:index]
                b = string[index:]
                assert_2(f1, f2, a, b, statistics1, statistics2)
        clock = time.perf_counter() - clock
        cpu = correct_cpu(time.process_time() - cpu)
        statistics = [v1 + v2 for v1, v2 in zip(statistics1, statistics2)]
        total = sum(statistics)
        print("%s %d %5.2f %5.2f  %9.2e %9.2e %8d "
              % (name, combined_string_length, clock, cpu,
                 clock/total, cpu/total, total), end='')
        if statistics1 == statistics2:
            print(statistics)
        else:
            print(statistics1, statistics2)


if __name__ == '__main__':
    print_platform()
    quick_tests(distance8)
    test_permutation_with_repetition(distance8, distance8)
