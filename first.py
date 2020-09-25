'Trying to see what async does when i try to crash it while it runs.'

import asyncio
import signal


def shutdown():
    'shutdown is signal handler for graceful shutdown of the application.'
    loop = asyncio.get_running_loop()
    
    '''
    This is required to remove the handler to avoid handling them again. 
    (bad idea if you don't)
    '''
    for sig_name in [signal.SIGINT, signal.SIGTERM]:
        loop.remove_signal_handler(sig_name)

    print("\nshutting down the application")

    '''
    Get all tasks in the event loop
    This is usually just the main loop as asyncio.run() usually handles
    cancellation of the tasks that you start from the main() event loop.
    '''
    task_count = [i for i in asyncio.all_tasks()]
    print("task count: ", len(task_count))

    '''
    cancel the tasks acquired in the step above.
    '''
    for task in asyncio.all_tasks():
        print(task.get_coro())
        task.cancel()


async def long_running_process(num):
    'LongRunningProcess.'
    try:
        while True:
            print("waiting...", num)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('Recieved cancel for long_running_process', num)
    

async def another_long_running_process(num):
    'Wow another long running process!'
    iterator = num
    try:
        while iterator > 0:
            await asyncio.sleep(1)
            print("another_long_running_process", iterator, "!")
    except asyncio.CancelledError:
        print('recieved cancel for another_long_running_process', num)


async def main():
    'Entry coroutine.'
    loop = asyncio.get_running_loop()
    task = asyncio.current_task()
    print(task.get_coro())

    '''
    register signals to be handled to gracefully shutdown the application.
    '''
    for sig_name in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig_name, shutdown)

    print("Started main coroutine")

    '''
    create tasks on the event loop to execute concurrently.
    '''
    for i in range(10):
        asyncio.create_task(long_running_process(i),
                            name="coro_task{}".format(i))
        asyncio.create_task(another_long_running_process(i),
                            name="another_coro_task{}".format(i))

    '''
    except the current task, await all the tasks in the event loop.
    '''
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            await task


if __name__ == '__main__':
    try:
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        print("Recieved a KeyboardInterrupt")
