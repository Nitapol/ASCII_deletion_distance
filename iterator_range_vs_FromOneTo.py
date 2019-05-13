class Range1inclusive(object):
    """
    Range1inclusive(stop[, step]) -> Range1inclusive object

    Return an iterator that produces a sequence of integers from 1 (inclusive)
    to stop (inclusive) by step. Range1inclusive(n) produces 1, 2, 3, ..., n.
    When step is given, it specifies the increment (or decrement).
    """
    def __init__(self, stop, step=1):
        self.number = 1
        self.stop = stop
        if step == 0:
            raise ValueError
        if stop >= 1:
            if step < 0:
                raise ValueError
        else:
            if step > 0:
                raise ValueError
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.step > 0:
            if self.number > self.stop:
                raise StopIteration
        else:
            if self.number < self.stop:
                raise StopIteration
        number = self.number
        self.number += self.step
        return number


if __name__ == '__main__':

    def count_and_assert(stop, step, expected):

        def assert_after_stop(test):
            if n != expected:
                print('Test "', test, '": stop=', stop, ', step=', step,
                      ' expected ', expected, ' counted', n, sep='')
                exit(1)

        def assert_iterator(test):
            j = 1 + (n - 1) * step
            if i != j:
                print('Test "', test, '": stop=', stop, ', step=', step,
                      ' expected ', j, ' iterator value is ', i, sep='')
                exit(1)

        t = 'Range1inclusive(stop, step)'
        n = 0
        for i in Range1inclusive(stop, step):
            n += 1
            assert_iterator(t)
        assert_after_stop(t)

        t = 'Range1inclusive(stop, step=step)'
        n = 0
        for i in Range1inclusive(stop, step=step):
            n += 1
            assert_iterator(t)
        assert_after_stop(t)

        if step == 1:
            t = 'Range1inclusive(stop)'
            n = 0
            for i in Range1inclusive(stop):
                n += 1
                assert_iterator(t)
            assert_after_stop(t)

        for s in ['stop, step', 'stop, step=step', 'stop']:

            code = """
t = 'Range1inclusive({0})'
n = 0
for i in Range1inclusive({0}):
    n += 1
    assert_iterator(t)
assert_after_stop(t)
        """.format(s)
            exec(code)


    def exeption_is_expected(stop, step):
        try:
            Range1inclusive(stop, step)
            print('Test "exeption_is_expected": stop = ', stop,
                  ', step = ', step, sep='')
            exit(1)
        except ValueError:
            pass

    def iterate_and_compare_to_range(stop, step, expected):
        i1 = Range1inclusive(stop, step)
        n = 0
        for j2 in range(1, stop + 1 if step >= 0 else stop - 1, step):
            try:
                j1 = next(i1)
            except StopIteration:
                print('Test "Compare to range" StopIteration: stop = ', stop,
                      ', step = ', step, ', n = ', n, sep='')
                exit(1)
            if j1 != j2:
                print('Test "Compare to range": stop = ', stop,
                      ', step = ', step, ', n = ', n,
                      ', j1 = ', j1, ', j2 = ', j2, sep='')
                exit(1)
            n += 1
            j = 1 + (n - 1) * step
            if j1 != j:
                print('Test "Compare to range": stop=', stop, ', step=', step,
                      ' expected ', j, ' iterator value is ', j1, sep='')
                exit(1)
        if n != expected:
            print('Test "Compare to range": stop=', stop, ', step=', step,
                  ' expected ', expected, ' counted', n, sep='')
            exit(1)
        try:
            next(i1)
            print('Test "Compare to range": Extra one stop=', stop, ', step=',
                  step, ' expected ', expected, ' counted', n, sep='')
            exit(1)
        except StopIteration:
            pass

    def sanity_test():
        count_and_assert(1, 1, 1)
        count_and_assert(2, 1, 2)
        count_and_assert(100, 2, 50)
        count_and_assert(0, -1, 2)
        count_and_assert(0, -1, 2)
        count_and_assert(-1, -2, 2)
        count_and_assert(-100, -2, 51)
        exeption_is_expected(1, 0)
        exeption_is_expected(3, -1)
        exeption_is_expected(100, -1)
        iterate_and_compare_to_range(1, 1, 1)
        iterate_and_compare_to_range(2, 1, 2)
        iterate_and_compare_to_range(100, 2, 50)
        iterate_and_compare_to_range(0, -1, 2)
        iterate_and_compare_to_range(0, -1, 2)
        iterate_and_compare_to_range(-1, -2, 2)
        iterate_and_compare_to_range(-100, -2, 51)
        print('Passed sanity_test!')

    sanity_test()

    exec('p_variable = [1,2,3,4]')
    global p_variable
    print(p_variable)

    from time import perf_counter_ns as timer
    limit = 1000
    n = 0
    clock0 = timer()
    for i in range(1, limit + 1):
        n += i
    clock1 = timer()
    print(clock1-clock0, n, i)

    n = 0
    clock0 = timer()
    for i in Range1inclusive(limit):
        n += i
    clock1 = timer()
    print(clock1-clock0, n, i)


n = 0
clock0 = timer()
for i in range(1, limit + 1):
    exec('n += i')
clock1 = timer()
print(clock1 - clock0, n, i)

n = 0
clock0 = timer()
exec('''
for i in Range1inclusive(limit):
    n += i
''')
clock1 = timer()
print(clock1 - clock0, n, i)

