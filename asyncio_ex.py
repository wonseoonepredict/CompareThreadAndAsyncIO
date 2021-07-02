import asyncio
import itertools
import sys
import math

count = 0

spinners = []

async def spin(msg: str, id: int):
    global count
    cnt0 = 0
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        count += 1
        cnt0 += 1
        cnt = 0
        for i in range(0, 1000000):
            cnt += math.sqrt(i)
        status = char + ' ' + msg + '[' + str(id) + '] ' + str(cnt0)
        #status = char + ' ' + msg + '[' + str(id) + '] '
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)  # 1
        except asyncio.CancelledError:  # 2
            break
    write(' ' * len(status) + '\x08' * len(status))

async def slow_function():  # 3
    await asyncio.sleep(20)  # 4
    return 42

def terminate():
    for spinner in spinners:
        spinner.cancel()

def noneconcurrent(cnt:int):
    tasks = []
    for i in range(0, cnt):
        #spinner = asyncio.create_task(spin('thinking!', i))  # 6
        spinner = asyncio.ensure_future(spin('thinking!', i))  # 6
        tasks.append(spinner)
    return tasks

async def concurrent(cnt:int):
    cbs = []
    for i in range(0, cnt):
        cbs.append(functools.partial(spin,'thinking!', i))
    L = await asyncio.gather(*[cb() for cb in cbs])

async def supervisor(cnt: int,concurrent:bool= False):  # 5
    global spinners
    if concurrent is False:
        results = noneconcurrent(cnt)
        spinners += results
    else:
        concurrent(cnt)
    result = await slow_function()  # 8
    terminate() # 9
        
    return result

def main(start: int, end: int, concurrent: bool = False):
    global count
    #loop = asyncio.get_event_loop()  # 10
    for i in range(start, end):
        print('ID    :', i)
        #result = loop.run_until_complete(supervisor(i))  # 11
        asyncio.run(supervisor(i))
        print('Count :', count)
        count = 0
    #loop.close()

if __name__ == '__main__':
    #main(start=1, end=4)
    #print("====")
    main(start=10, end=12, concurrent=True)
