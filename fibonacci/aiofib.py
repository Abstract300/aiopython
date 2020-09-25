'''
asyncIO fibonacci number calculator
TIME: python aiofib.py  0.38s user 0.02s system 78% cpu 0.500 total
'''
import asyncio


async def fib(num):
    'fibnocci number calculator'
    await asyncio.sleep(0.100)
    a, b = 0, 1
    for i in range(num):
        a,b = b, a+b
    print("Fibonacci at {0}: {1}".format(num, a))


async def main():
    task = [fib(10000) for i in range(100)]
    await asyncio.gather(*task)


asyncio.run(main())
