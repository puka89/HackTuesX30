import tornado.ioloop as ioloop
import tornado.web as web
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler as ws
from RPi import GPIO
from time import sleep
from threading import Thread
import random
from asyncio import Queue
import json
from ds18b20 import DS18B20
from tornado import gen
import tornado.queues

class GameHandler(RequestHandler):
    def get(self):
        self.render("./static/views/index.html")

class GameWebSocket(ws):
    def open(self):
        clients.append(self)
        print("connected")

    def on_message(self, message):
        pass

    def close(self):
        print("disconnected")

GPIO.setmode(GPIO.BOARD)
player = ""
clients = []
answer = ""
player_turn = 1
removed_pawn_id = ""

state = {
    31 : "high",
    8 : "high",
    40 : "high",
    38 : "high",
    36 : "low",
    18 : "high",
    16 : "high",
    33 : "low",
    37 : "high",
    26 : "high",
    24 : "high",
    5 : "low",
    10 : "high",
    32 : "high",
    35 : "low",
    22 : "high",
    29 : "high",
    3 : "high",
    11 : "high"
}

dice_flag = 0
answer_flag = 0
start_game_flag = 1
move_flag = 0

playing = ["03172455d7ff", "0317243e28ff", "03172459f6ff", "0317243c31ff"]

answers = {
    3 : "False",
    11 : "True"
}

players = {
    "red" : 10,
    "black" : 10,
    "white" : 10,
    "yellow" : 10
}

queue = Queue()
front_end_queue = tornado.queues.Queue()

gpio_fields = {
    32 : 1,
    31 : 2,
    33 : 3,
    26 : 4,
    37 : 5,
    24 : 6,
    5 : 7,
    10 : 8,
    38 : 9,
    8 : 10,
    35 : 11,
    18 : 12,
    16 : 13,
    22 : 14,
    36 : 15,
    40 : 16,
    29 : 21,
    3 : 22,
    11 : 23
}

sensors_dict = {
    "03172455d7ff" : "red",
    "0317243e28ff" : "black",
    "03172459f6ff" : "white",
    "0317243c31ff" : "yellow"
}

positions = {
    1 : "03172455d7ff",
    2 : "",
    3 : "",
    4 : "",
    5 : "0317243e28ff",
    6 : "",
    7 : "",
    8 : "",
    9 : "03172459f6ff",
    10 : "",
    11 : "",
    12 : "",
    13 : "0317243c31ff",
    14 : "",
    15 : "",
    16 : ""
}

fields_status = random.shuffle(['red', 'red', 'red', 'red', 'red', 'red', 'red',
                             'red', 'red', 'red', 'g', 'g', 'g', 'g', 'g', 'g'])

def make_app():
    return web.Application([
        (r"/", GameHandler),
        (r"/index", GameWebSocket),
    ])

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

dice_value = "-"
question = "-"

def start_game():
    print("start")
    global start_game_flag
    start_game_flag = 0
    global dice_flag 
    dice_flag = 1
    gpio_revent()
    sleep(2)
    b1_add()
    print("started")

def roll_dice():
    global dice_flag
    global move_flag
    global dice_value
    dice_flag = 0
    move_flag = 1
    print("roll")
    sleep(2)
    gpio_events()
    dice_value = random.randint(1, 6)

def read_w1_bus():
    print("read_w1")
    sensor_ids = []
    sensors_temp = DS18B20.get_all_sensors()
    for sensor in sensors_temp:
        sensor_ids.append(sensor.get_id())

    return sensor_ids

def blocking_debounce():
    low_count = 0
    high_count = 0
    while True:
        while not queue.empty():
            pin = queue.get_nowait()

            while True:
                if high_count == 3:
                    if move_flag == 1 and state[pin] != "high":
                        print("pulling")
                        pulling_event(pin)
                    state[pin] = "high"
                    gpio_events()
                    low_count = 0
                    high_count = 0
                    break

                if low_count == 3:
                    state[pin] = "low"
                    print(start_game_flag)
                    if start_game_flag == 1:
                        start_game()
                    elif dice_flag == 1:
                        roll_dice()
                    elif move_flag == 1:
                        print("putting")
                        putting_event(pin)
                    elif answer_flag == 1:
                        print("lul answer")
                        received_answer(pin)
                    low_count = 0
                    high_count = 0
                    break

                if GPIO.input(pin) == GPIO.LOW:
                    low_count += 1
                else:
                    high_count += 1

                sleep(0.1)

def handle_gpio(pin):
    print(pin)
    gpio_revent()
    queue.put_nowait(pin)

def pulling_event(pin):
    sleep(3)
    print("pulling")
    global removed_pawn_id
    global positions
    current = read_w1_bus()
    removed_pawn_id = diff(playing, current)
    print(removed_pawn_id)
    print(gpio_fields[pin])
    positions[gpio_fields[pin]] = ""

def putting_event(pin):
    sleep(3)
    global removed_pawn_id
    global player
    global positions
    global fields_status
    global gpio_fields
    global sensors_dict
    global move_flag
    global dice_flag
    global player_turn

    positions[gpio_fields[pin]] = removed_pawn_id
    print(fields_status)
    print(gpio_fields[pin])
    if random.randint(1, 2) == 2:
        player = sensors_dict[removed_pawn_id[0]]
        prompt_question()
    else:
        print("roll")
        move_flag = 0
        dice_flag = 1
        player_turn += 1
        b1_add()
    removed_pawn_id = ""

def prompt_question():
    global question
    global answer
    print("question")
    keys = ["one", "two"]
    data = json.load(open("questions.json", "r"))
    question_list = data[keys[random.randint(0, 1)]]
    question = question_list["question"]
    answer = question_list["answer"]

    answer_lock()

def send_message(message):
    #print("send " + message)
    for client in clients:
        client.write_message(message)

def answer_lock():
    print("lockA")
    sleep(1)
    global move_flag
    global answer_flag
    answer_flag = 1
    move_flag = 0
    gpio_revent()
    GPIO.add_event_detect(3, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(11, GPIO.BOTH, handle_gpio)

def answer_unlock():
    print("ulockA")
    sleep(1)
    global answer_flag
    global dice_flag
    answer_flag = 0
    dice_flag = 1
    GPIO.remove_event_detect(3)
    GPIO.remove_event_detect(11)
    b1_add()

def received_answer(pin):
    print("check answer")
    global players
    global player_turn
    if answers[pin] != answer:
        players[player] -= 1

    answer_unlock()
    player_turn += 1

def gpio_setup():
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def gpio_events():
    print("add")
    GPIO.add_event_detect(31, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(8, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(40, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(38, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(36, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(18, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(16, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(33, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(37, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(26, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(24, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(5, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(10, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(32, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(35, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(22, GPIO.BOTH, handle_gpio)

def gpio_revent():
    print("remove")
    GPIO.remove_event_detect(31)
    GPIO.remove_event_detect(8)
    GPIO.remove_event_detect(40)
    GPIO.remove_event_detect(38)
    GPIO.remove_event_detect(36)
    GPIO.remove_event_detect(18)
    GPIO.remove_event_detect(16)
    GPIO.remove_event_detect(33)
    GPIO.remove_event_detect(37)
    GPIO.remove_event_detect(26)
    GPIO.remove_event_detect(24)
    GPIO.remove_event_detect(5)
    GPIO.remove_event_detect(10)
    GPIO.remove_event_detect(32)
    GPIO.remove_event_detect(35)
    GPIO.remove_event_detect(22)
    GPIO.remove_event_detect(29)
    GPIO.remove_event_detect(3)
    GPIO.remove_event_detect(11)

def b1_add():
    print("addB")
    GPIO.add_event_detect(29, GPIO.BOTH, handle_gpio)

import datetime
@gen.coroutine
def socket_queue():
    while True:
        send_message('{"player" : { "red" : %s, "black" : %s, "white" : %s, "yellow" : %s}, "turn" : %s, "dice" : "%s", "question" : "%s" }' % (players['red'],
        players['black'],
        players['white'],
        players['yellow'],
        player_turn,
        dice_value,
        question))

        yield gen.Task(ioloop.IOLoop.current().add_timeout, datetime.timedelta(milliseconds=500))

@gen.coroutine
def main():
    gpio_setup()
    b1_add()
    blocking_debounce_thread = Thread(target=blocking_debounce)
    blocking_debounce_thread.start()

    app = make_app()
    app.listen(8888)

    socket_queue()
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
