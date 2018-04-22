from asyncio import Queue
from threading import Thread
import time
import asyncio

queue = Queue()

def thr():
    count = 0
    last_event = ""
    while True:
        while not queue.empty():
            if count == 3:
                print("interrupted")
                count = 0

            event = queue.get_nowait()
            if event == last_event:
                count += 1
            else:
                last_event = event
                count = 1
            time.sleep(0.1)

async def add():
    await queue.put("high")

thread = Thread(target=thr)
thread.start()
add()
