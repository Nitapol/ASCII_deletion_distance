# The subset sum problem:
#
# Given an array of N integers, check if it is possible to obtain a sum of S,
# by choosing some (or none) elements of the array and adding them.
#
# This code contributors are Alexander Lopatin, Sahil Shelangia, DYZ


def if_possible_sum_obvious(a, s):
    if a is None or len(a) == 0:
        return s == 0
    if s > 0:
        if s > sum([i for i in a if i > 0]):
            return False
    elif s < 0:
        if s < sum([i for i in a if i < 0]):
            return False
    else:
        for i in a:
            if i == 0:
                return True
        else:
            return False
    return None


def is_possible_sum_dynamic(a, s):  # Dynamic Programming
    if a is None or len(a) == 0:
        return s == 0
    n = len(a)
    b = [[False for _ in range(s + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        b[i][0] = True
    for i in range(1, s + 1):
        b[0][i] = False
    for i in range(1, n + 1):
        for j in range(1, s + 1):
            if j < a[i - 1]:
                b[i][j] = b[i - 1][j]
            if j >= a[i - 1]:
                b[i][j] = (b[i - 1][j] or b[i - 1][j - a[i - 1]])
    return b[n][s]


def is_possible_sum_combinations(a, s):  # combinations from itertools
    check_obvious = if_possible_sum_obvious(a, s)
    if check_obvious is not None:
        return check_obvious
    from itertools import combinations
    for r in range(len(a)):
        for combo in combinations(a, r + 1):
            if sum(combo) == s:
                return True
    return False


if __name__ == '__main__':
    import time
    for f in [is_possible_sum_dynamic, is_possible_sum_combinations]:
        print('\nTesting function:', f.__name__)
        for N in range(40):
            a_global = [i+1 for i in range(N)]
            sum2check = sum(a_global)
            print(N, end='')

            def time_and_check(f_local, sum_local, expected):
                t0 = time.perf_counter_ns()
                possible = f_local(a_global, sum_local)
                t1 = time.perf_counter_ns() - t0
                print('', t1, sep=',', end='' if expected else '\n')
                if possible != expected:
                    print('Not possible! Strange')
                    print(sum_local, a_global, sep='\n')
                    exit(1)

            time_and_check(f, sum2check, True)
            time_and_check(f, sum2check + 1, False)
