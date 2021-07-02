import threading
import itertools
import time
import sys
import math

count = 0
#lock = threading.Lock()

class Signal:  # 1
    go = True

#class Result:
#    id: int
#    cnt: int
#
#    def __init__(self, id:int, cnt:int):
#        self.id = id
#        self.cnt = cnt
#

spinners = []
temp_signal=None

#results = []

def spin(msg: str, signal: Signal, id: int):  # 2
    global count
    cnt0 = 0
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # 3
        #lock.acquire()
        count += 1
        #ock.release()
        cnt0 += 1
        cnt = 0
        for i in range(0, 1000000):
            cnt += math.sqrt(i)
        status = char + ' ' + msg + '[' + str(id) + '] ' + str(cnt0)
        write(status)
        #print(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:  # 4
            break
    #results.append(Result(id, cnt0))
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():  # 5
    # pretend waiting a long time for I/O
    time.sleep(20)  # 6
    return 42

def terminate():
    if temp_signal is not None:
        temp_signal.go = False  # 11

    for spinner in spinners:
        spinner.join()  # 12


def supervisor(cnt: int):  # 7
    global spinners
    global temp_signal

    signal = Signal()
    temp_signal = signal

    for i in range(0, cnt):
        spinner = threading.Thread(target=spin,
                                  args=('thinking', signal, i))

        spinners.append(spinner)

    for spinner in spinners:
        spinner.start()  # 9

    result = slow_function()  # 10

    terminate()

    spinners.clear()

    return result

def main(start: int, end: int):
    global count
    for i in range(start, end):
        print('id    :', i)
        result = supervisor(i)  # 13
        print('Count :', count)
        count = 0
        print('\n')

if __name__ == '__main__':
    main(0, 8)
