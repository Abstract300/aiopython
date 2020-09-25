'''
sync fibonacci number calculator
TIME: python syncfib.py  0.92s user 0.03s system 8% cpu 10.988 total
'''
import time


def fib(num):
    'fibnocci number calculator'
    time.sleep(0.100)
    a, b = 0, 1
    for i in range(num):
        a,b = b, a+b
    return "Fibonacci at {0}: {1}".format(num, a)


task = [fib for i in range(100)]

for t in task:
    print(t(10000))
