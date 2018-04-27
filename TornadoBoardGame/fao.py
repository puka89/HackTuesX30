from RPi import GPIO
from time import sleep
from asyncio import Queue
from threading import Thread

GPIO.setmode(GPIO.BOARD)

queue = Queue()
answer_flag = 0
state = {
    16 : "high",
    18 : "high"
}

def blocking_debounce():
    low_count = 0
    high_count = 0
    while True:
        while not queue.empty():
            pin = queue.get_nowait()

            for i in range(10):
                if high_count == 3:
                    if not answer_flag and state[pin] != "high":
                        print("visok bez")
                        state[pin] = "high"
                        #pulling_event(pin)
                    GPIO.add_event_detect(16, GPIO.BOTH, handle_gpio)
                    GPIO.add_event_detect(18, GPIO.BOTH, handle_gpio)
                    low_count = 0
                    high_count = 0
                    break

                if low_count == 3:
                    state[pin] = "low"
                    if answer_flag != 1:
                        print("nisko bez")
                        #putting_event(pin)
                    if answer_flag == 1:
                        print("nisko otgovor")
                        #received_answer(pin)
                    GPIO.add_event_detect(16, GPIO.BOTH, handle_gpio)
                    GPIO.add_event_detect(18, GPIO.BOTH, handle_gpio)
                    low_count = 0
                    high_count = 0
                    break

                if GPIO.input(pin) == GPIO.LOW:
                    low_count += 1
                else:
                    high_count += 1

                sleep(0.1)

def handle_gpio(pin):
    GPIO.remove_event_detect(16)
    GPIO.remove_event_detect(18)
    print(pin)
    queue.put_nowait(pin)

if __name__ == '__main__':
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(16, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(18, GPIO.BOTH, handle_gpio)

    blocking_debounce_thread = Thread(target=blocking_debounce)
    blocking_debounce_thread.start()
