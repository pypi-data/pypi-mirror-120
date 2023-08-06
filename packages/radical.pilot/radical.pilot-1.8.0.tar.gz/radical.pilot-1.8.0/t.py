#!/usr/bin/env python3

import time
import queue
import threading as mt

N = 1024 * 1024


def read(q):

    start = time.time()
    try:
        while True:
            i = q.get()
            if i == N - 1:
                break
    except:
        pass
    finally:
        print('read : %10.2fs' % (time.time() - start))


def write(q):

    start = time.time()
    try:
        for i in range(N):
            q.put(i)
    except:
        pass
    finally:
        print('write: %10.2fs' % (time.time() - start))


def main():

    q = queue.Queue()

    reader = mt.Thread(target=read,  args=[q])
    writer = mt.Thread(target=write, args=[q])

    reader.daemon = True
    writer.daemon = True

    reader.start()
    writer.start()

    reader.join()
    writer.join()


if __name__ == '__main__':

    main()


