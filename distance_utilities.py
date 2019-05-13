import platform
import sys


def fee(char): return ord(char)


def assert_1(f, a, b, c):
    e = 0
    for char in c:
        e += fee(char)
    d = f(a, b)
    if d != e:
        print("*** Error in the expected distance : '",
              a, "', '", b, "', ", e, '!=', d, ' ', f.__name__, sep='')
        exit(1)

def assert_2(f1, f2, a, b, s1 = None, s2 = None):
    d1 = f1(a, b, statistics=s1)
    d2 = f2(b, a, statistics=s2)
    if d1 != d2:
        print("*** Error in the expected distance : '",
              a, "' , '", b, "', ", d1, '!=', d2, ' ', f1.__name__, ' ',
              '' if f1.__name__ == f2.__name__  else f2.__name__, sep='')
        exit(1)


def print_platform():
    print(platform.node())
    (mac_ver, _, _) = platform.mac_ver()
    print(platform.python_version_tuple())
    if mac_ver is not None and mac_ver != "":
        print("macOS version", mac_ver)
    print(platform.platform())
    print("Python", platform.python_build(), platform.python_compiler())
    print("Executing in", "64bit" if sys.maxsize > 2 ** 32 else "32bit")


def correct_cpu(cpu_time):
    pv1, pv2, _ = platform.python_version_tuple()
    pcv = platform.python_compiler()
    if pv1 == '3' and '5' <= pv2 <= '8' and pcv == 'Clang 6.0 (clang-600.0.57)':
        cpu_time /= 2.0
    return cpu_time
