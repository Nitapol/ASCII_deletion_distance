# from multiprocessing import Process
#
#
# def print_func(continent='Asia'):
#     print('The name of continent is : ', continent)
#
# if __name__ == "__main__":  # confirms that the code is under main function
#     names = ['America', 'Europe', 'Africa']
#     procs = []
#     proc = Process(target=print_func)  # instantiating without any argument
#     procs.append(proc)
#     proc.start()
#
#     # instantiating process with arguments
#     for name in names:
#         # print(name)
#         proc = Process(target=print_func, args=(name,))
#         procs.append(proc)
#         proc.start()
#
#     # complete the processes
#     for proc in procs:
#         proc.join()
#


import multiprocessing
import time
import signal
import sys

jobs = []

def worker():
    signal.signal(signal.SIGINT, signal_handler)
    n = 0
    while(True):
        n += 1
        time.sleep(1.1234)
        print("Working...", n)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    # for p in jobs:
    #     p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    for i in range(50):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()

# import multiprocessing
# import time
# import signal
#
# def init_worker():
#     signal.signal(signal.SIGINT, signal.SIG_IGN)
#
# def worker():
#     n = 0
#     while(True):
#         n += 1
#         time.sleep(1.1234)
#         print("Working...", n)
#
# if __name__ == "__main__":
#     pool = multiprocessing.Pool(50, init_worker)
#     try:
#         for i in range(50):
#             pool.apply_async(worker)
#
#         time.sleep(10)
#         pool.close()
#         pool.join()
#
#     except KeyboardInterrupt:
#         print("Caught KeyboardInterrupt, terminating workers")
#         pool.terminate()
#         pool.join()
