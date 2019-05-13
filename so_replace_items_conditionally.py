import numpy as np
import itertools
import time
import platform


def f1():  # answered by Alexander Lopatin #####################################
    n = []
    t = [3.8856, 4.1820, 2.3040, 1.0197,  0.4295,
         1.5178, 0.3853, 4.2848, 4.30911, 3.2299,
         1.8528, 0.6553, 3.3305, 4.1504,  1.8787]
    x = 5./7.
    p = list(itertools.product([0, 1], repeat=5))
    for y in t:
        j = int(y/x)
        if x*j < y < x*(j+1):
            n.append(p[j])
    return np.asarray(n).reshape(len(t), 5)


def f2():  # original post by motaha ###########################################
    n = []
    t = [3.8856, 4.1820, 2.3040, 1.0197, 0.4295,
         1.5178, 0.3853, 4.2848, 4.30911,3.2299,
         1.8528, 0.6553, 3.3305, 4.1504, 1.8787]
    z = np.linspace(0,5,8)
    for i in t:
        if i>=z[0] and i<z[1]:
            n.extend([0,0,0,0,0])
        elif i>=z[1] and i<z[2]:
            n.extend([0,0,0,0,1])
        elif i>=z[2] and i<z[3]:
            n.extend([0,0,0,1,0])
        elif i>=z[3] and i<z[4]:
            n.extend([0,0,0,1,1])
        elif i>=z[4] and i<z[5]:
            n.extend([0,0,1,0,0])
        elif i>=z[5] and i<z[6]:
            n.extend([0,0,1,0,1])
        elif i>=z[6] and i<z[7]:
            n.extend([0,0,1,1,0])
    return np.asarray(n).reshape(len(t),5)


def f3(): # answered by Kostas Mouratidis ######################################
    n = []
    t = [3.8856, 4.1820, 2.3040, 1.0197, 0.4295,
         1.5178, 0.3853, 4.2848, 4.30911,3.2299,
         1.8528, 0.6553, 3.3305, 4.1504, 1.8787]
    z = np.linspace(0,5,8)
    bins = np.digitize(t, z) - 1  # minus 1 just to align our shapes
    patterns = np.array([
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 1],
    ])
    inds = np.zeros((len(t), len(z) - 1), dtype=int)
    inds[np.arange(len(t)), bins] = 1
    inds = inds @ patterns
    return inds

# Testing ... ##################################################################


def correct_cpu(cpu_time):
    pv1, pv2, _ = platform.python_version_tuple()
    pcv = platform.python_compiler()
    if pv1 == '3' and '5' <= pv2 <= '8' and pcv == 'Clang 6.0 (clang-600.0.57)':
        cpu_time /= 2.0
    return cpu_time


def test(test_function, test_loops, test_name):
    t = time.perf_counter()
    c = time.process_time()
    test_result = []
    for j in range(0, test_loops):
        test_result = test_function()
    t = time.perf_counter() - t
    c = correct_cpu(time.process_time() - c)
    print('%.4f  %.4f %s' % (t, c, test_name))
    return test_result

print('Python version  :', platform.python_version())
print('       build    :', platform.python_build())
print('       compiler :', platform.python_compiler())
print()
loops = 100000
f2test = [(f1, 'proposed by Alexander Lopatin'),
          (f2, 'original by motaha'),
          (f3, 'proposed by Kostas Mouratidis')]
print('Time    CPU for', loops, 'loops')

results = []
for func, name in f2test:
    results.append(test(func, loops, name))

original = 1
_, name = f2test[original]
print('\nthe final pattern I want! ' + name)
print(results[original])
for order, result in enumerate(results):
    if order == original:
        continue
    _, name = f2test[order]
    error = False
    for i_row, row in enumerate(result):
        for j_column, value in enumerate(row):
            if value != results[original][i_row][j_column]:
                error = True
                print('\n*** Check for ERRORS in (%d,%d) %s '
                      % (i_row, j_column, name))
                break
        if error:
            break
    if error:
        print(result)
    else:
        print('The same ' + name)
