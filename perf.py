import argparse
import signal
import os

from asyncio_ex import main as asyncio_main
from asyncio_ex import terminate as asyncio_term
from thread_ex import main as thread_main
from thread_ex import terminate as thread_term

thread_cb = ["thread", thread_main]
asyncio_cb = ["asyncio", asyncio_main]
thread_term = ["thread", thread_term]
asyncio_term = ["asyncio", asyncio_term]

methods={"thread":[thread_cb],
         "asyncio":[asyncio_cb],
         "all":[thread_cb, asyncio_cb]}

terms={"thread":[thread_term],
       "asyncio":[asyncio_term],
       "all":[thread_cb, asyncio_term]}

type="asyncio"

catch_signals = [signal.SIGINT,signal.SIGPIPE, signal.SIGSEGV,signal.SIGTERM]

def handler(signum, frame):
    if signum in catch_signals:
        print('-----------------------/')
        print('perf will be terminated')
        print('-----------------------/')
        for term in terms[type]:
            term[1]()
        exit()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--range', metavar='N', type=int, nargs='+',
                        help='an integer for start thread count')
    parser.add_argument('--type',dest ='type', type=str)

    args = parser.parse_args()

    start = 0
    end = 0

    if len(args.range) == 1:
        start = int(args.range[0])
        end = start + 1
    elif len(args.range) > 1:
        start = int(args.range[0])
        end = int(args.range[1]) + 1

    if start < 1:
        if end == 1:
            exit()
        elif end > 1:
            start += 1

    type = args.type

    print("perf " + type + " " + str(start) + " " + str(end))

    for sig in catch_signals:
        signal.signal(sig, handler)

    for cb in methods[type]:
        print('test = ', cb[0])
        cb[1](start=start, end=end)
