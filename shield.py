'''
this script helps understand about `asyncio.shield`
'''
import asyncio


async def super_coro(num):
    try:
        await asyncio.shield(sub_coro(69))
    except asyncio.CancelledError:
        print("super task cancelled.", num)


async def sub_coro(num):
    n = 0
    try:
        while n < 5:
            print("sub task.. ", num)
            await asyncio.sleep(1)
            n = n+1
        print("DONE DOING SUB TASK!")
    except asyncio.CancelledError:
        print('sub task cancelled.')


async def main():
    tsk = asyncio.create_task(super_coro(420))

    await asyncio.sleep(2)

    tsk.cancel()

    try:
        await tsk
        await asyncio.sleep(6)
    except asyncio.CancelledError:
        print('main coroutine cancelled.')


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('keyboard interrupt occuered.')
