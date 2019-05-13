import time
import timeit
import numpy as np
import platform


def correct_cpu(cpu_time):
    pv1, pv2, _ = platform.python_version_tuple()
    pcv = platform.python_compiler()
    if pv1 == '3' and '5' <= pv2 <= '8' and pcv == 'Clang 6.0 (clang-600.0.57)':
        cpu_time /= 2.0
    return cpu_time


def test(func, n, f, name):
    print('\nTested %s :' % name)
    print('Size   Time     CPU   MFLOPS')
    for i in range(90, 101):
        t = time.perf_counter()
        c = time.process_time()
        tm = func(i, n)
        t = time.perf_counter() - t
        c = correct_cpu(time.process_time() - c)
        st = t if tm <= 0.0 else tm
        flops = f * 2 * float(i) ** 2 * float(n) / st / 1000000.0
        print('%3d  %.4f  %.4f  %7.2f' % (i, st, c, flops))
        if abs(t-st)/st > 0.02:
            print('    +%.4f' % t)

def test0(i0, i1):
    a, b = np.random.rand(i0, i0), np.random.rand(i0)
    c = np.zeros(i0)
    for _ in range(i1):
        for i in range(i0):
            d = 0.0
            for j in range(i0):
                d += a[i][j]*b[j]
            c[i] = d
        np.matmul(a, b)
    return 0.0


def test1(i, n):
    a, b = np.random.rand(i, i), np.random.rand(i)
    for _ in range(n):
        np.matmul(a, b)
    return 0.0


def test2(i, n):
    s = 'import numpy as np;' + \
        'a, b = np.random.rand({0},{0}), np.random.rand({0})'
    s = s.format(i)
    r = 'np.matmul(a, b)'
    t = timeit.repeat(stmt=r, setup=s, number=n)
    return sum(t)


def test3(i, n):
    s = 'import numpy as np;' + \
        'a, b = np.random.rand({0},{0}), np.random.rand({0})'
    s = s.format(i)
    r = 'np.matmul(a, b)'
    return timeit.timeit(stmt=r, setup=s, number=n)


print('Python version  :', platform.python_version())
print('       build    :', platform.python_build())
print('       compiler :', platform.python_compiler())
num = 10000
test(test0, num // 100, 1.0, 'by Python code. Multiply time by 500 to compare')
test(test1, 5 * num,    1.0, 'by Python code, math by numpy')
test(test2, num,        5.0, 'with timeit.repeat')
test(test3, 5 * num,    1.0, 'with timeit.timeit')
