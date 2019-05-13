a, b = 'a', 'b'


def f1(a, b):
    def f():
        nonlocal a, b
        print('\nf1\n1.', a, b)
        a, b = b, a
        print('2.', a, b)
    f()

f1(a, b)
print('3.', a, b, 'All changes in local f1 scope.')


def f2(a, b):
    def f2():
        global a, b
        print('\nf2\n1.', a, b)
        a, b = b, a
        print('2.',a, b)
    f2()


f2(a, b)
print('3.', a, b, 'Were changed in global scope.')


def f3():
    a, b = 'x', 'z'
    print('\nf3\n1.', a, b)
    a, b = b, a
    print('2.', a, b)


f3()
print('3.', a, b,  'All changes in local f1 scope.')


def f4():
    global a, b
    a, b = 'x','z'
    print('\nf4\n1.', a, b)
    a, b = b, a
    print('2.', a, b)


f4()
print('3.', a, b, 'Were changed in global scope.')


def f5(b, a):
    c = a
    d = b

    def f():
        global a, b
        print('\nf5\n1.', a, b)
        a, b = c, d
        print('2.', a, b)
    f()


f5('b', 'a')
print('3.', a, b, 'Were changed in global scope.')
