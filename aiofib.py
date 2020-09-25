'''
asyncio fibonacci calculator.
1, 1, 2, 3, 5, 8, 13 .....

num = 5
=>fib(3) + fib(2)
=>(fib(2) + fib(1)) + (fib(1) + fib(1))
=>((fib(1) + fib(1)) + 1) + (1 + 1)
=>((1 + 1) + 1) + (1 + 1)
=> 1 + 1 + 1 + 1 + 1
=> 5
'''

import asyncio
import signal


def shutdown():
    print("got signal")
    loop = asyncio.get_running_loop()
    
    for sig_name in [signal.SIGINT, signal.SIGTERM]:
        loop.remove_signal_handler(sig_name)

    print("\nshutting down the application")

    task_count = [i for i in asyncio.all_tasks()]
    print("task count: ", len(task_count))

    for task in asyncio.all_tasks():
        print(task.get_coro())
        task.cancel()


async def fib(num):
    'fibnocci number calculator'
    if num <= 1:
        return num
    return (await fib(num - 1)) + (await fib(num - 2))


async def fib_gatherer(fib_func, num):
    try:
        print("Fibonacci number at location *{0}* is *{1}*".format(num, await fib_func(num)))
    except asyncio.CancelledError:
        print("OOPSIES: ", num)


async def main():
    'main coroutine.'
    loop = asyncio.get_running_loop()
    
    for sig_name in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig_name, shutdown)

    _ = [asyncio.create_task(fib(num)) for num in range(30, 40, 1)]

    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            print(await task)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Recieved unhandled keyboard interrupt")
