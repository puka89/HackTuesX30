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

state = {
    31 : "high",
    8 : "high",
    40 : "high",
    38 : "high",
    36 : "high",
    18 : "high",
    16 : "high",
    33 : "high",
    37 : "high",
    26 : "high",
    24 : "high",
    5 : "high",
    10 : "high",
    32 : "high",
    35 : "high",
    22 : "high",
    29 : "high",
    3 : "high",
    11 : "high"
}

dice_flag = 0
answer_flag = 0
start_game_flag = 1

playing = ["03172455d7ff", "0317243e28ff", "03172459f6ff", "0317243c31ff"]

answers = {
    3 : "False"
    11 : "True"
}

players = {
    "red" : 10,
    "black" : 10,
    "white" : 10,
    "yellow" : 10
}

queue = Queue()

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
    "1" : "03172455d7ff",
    "2" : "",
    "3" : "",
    "4" : "",
    "5" : "0317243e28ff",
    "6" : "",
    "7" : "",
    "8" : "",
    "9" : "03172459f6ff",
    "10" : "",
    "11" : "",
    "12" : "",
    "13" : "0317243c31ff",
    "14" : "",
    "15" : "",
    "16" : ""
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

def start_game():
    start_game_flag = 0
    gpio_events()

    for client in clients:
        client.write_message({"turn" : player_turn})

def roll_dice():
    dice_flag = 0
    move_flag = 1

    for client in clients:
        client.write_message({"dice" : random.randint(1, 6)})

def read_w1_bus():
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

            for i in range(10):
                if high_count == 3:
                    if move_flag == 1 and state[pin] != "high":
                        pulling_event(pin)

                    state[pin] = "high"
                    gpio_events()
                    low_count = 0
                    high_count = 0
                    break

                if low_count == 3:
                    state[pin] = "low"
                    if start_game_flag == 1:
                        start_game()
                    if dice_flag == 1:
                        roll_dice()
                    if move_flag == 1:
                        putting_event()
                    if answer_flag == 1:
                        received_answer(pin)
                    gpio_events()
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
    sleep(0.7)
    current = read_w1_bus()
    removed_pawn_id = diff(playing, current)
    print(removed_pawn_id)
    print(gpio_fields[pin])
    positions[gpio_fields[pin]] = ""

def putting_event(pin):
    sleep(0.7)
    positions[gpio_fields[pin]] = removed_pawn_id

    if fields_status[int(gpio_fields[pin])] == 'red':
        player = sensors_dict[removed_pawn_id]
        prompt_question()

    removed_pawn_id = ""

def prompt_question():
    data = json.load(open("questions.json", "r"))
    question_list = data[random.randint(1, 10)]
    question = question_list[0]
    answer = question_list[1]

    send_message(question)
    answer_lock()

def send_message(message):
    for client in clients:
        client.write_message(message)

def answer_lock():
    GPIO.add_event_detect(3, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(11, GPIO.BOTH, handle_gpio)
    GPIO.remove_event_detect(29)

def answer_unlock():
    answer_flag = 0
    dice_flag = 1
    GPIO.remove_event_detect(3)
    GPIO.remove_event_detect(11)
    GPIO.add_event_detect(29, GPIO.BOTH, handle_gpio)

def received_answer(pin):
    if answers[pin] != answer:
        players[player] -= 1

    answer_unlock()
    player_turn += 1
    for client in clients:
        client.write_message({ "players" : players, "turn" : player_turn})

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
    GPIO.add_event_detect(29, GPIO.BOTH, handle_gpio)

def main():
    gpio_setup()
    b1_add()
    blocking_debounce_thread = Thread(target=blocking_debounce)
    blocking_debounce_thread.start()

    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
