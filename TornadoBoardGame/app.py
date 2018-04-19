import tornado.ioloop as ioloop
import tornado.web as web
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler as ws
from RPi import GPIO
from time import sleep
from threading import Thread
import random

GPIO.setmode(GPIO.BOARD)
clients = []

current = []
playing = ["03172455d7ff", "0317243e28ff", "03172459f6ff", "0317243c31ff"]

sensors_dict = {
	"03172455d7ff" : "red",
	"0317243e28ff" : "black",
	"03172459f6ff" : "white",
	"0317243c31ff" : "yellow"
}

fields_gpio = {
	"1" : 36,
	"2" : 38,
	"3" : 40,
	"4" : 31,
	"5" : 15,
	"6" : 23,
	"7" : 21,
	"8" : 19,
	"9" : 5,
	"10" : 18,
	"11" : 16,
	"12" : 12,
	"13" : 11,
	"14" : 13,
	"15" : 22,
	"16" : 32,
}

fields_status = random.shuffle(['red', 'red', 'red', 'red', 'red', 'red', 'red',
							 'red', 'red', 'red', 'g', 'g', 'g', 'g', 'g', 'g'])

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
	"16" : "",
}

buttons_gpio = {
	"1" : 29,
	"2" : 33,
	"3" : 35
}

dice_flag = 0
answer_flag = 0
start_game_flag = 0

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

def make_app():
    return web.Application([
        (r"/", GameHandler),
        (r"/index", GameWebSocket),
    ])


def gpio_setup():
    GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_w1_bus():
    while True:
	sensor_ids = []
	sensors_temp = DS18B20.get_all_sensors()
	for sensor in sensors_temp:
	    sensor_ids.append(sensor.get_id())

	current = sensor_ids
	time.sleep(.4)

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def print_state(data):
	#assuming no interrupt on pull out
	sensor_id = diff(playing, current)
	positions[data] = sensor_id
	print(data)
    time.sleep(1)

def start_game():
	pass

def roll_dice():
	pass

def answer_true():
	pass

def answer_false():
	pass

def button_1(data):
	if start_game_flag == 1:
		start_game()
		start_game_flag = 0
	elif dice_flag == 1:
		roll_dice()
		dice_flag = 0

def button_false(data):
    if answer_flag == 1:
		answer_false()
		answer_flag = 0

def button_true (data):
	if answer_flag == 1:
		answer_true()
		answer_flag = 0

def main():
    #setup gpios
    gpio_setup()

    GPIO.add_event_detect(36, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(38, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(40, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(31, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(15, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(23, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(21, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(19, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(5, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(18, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(16, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(12, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(11, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(13, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(22, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(32, GPIO.FALLING, print_state, bouncetime=1000)
    GPIO.add_event_detect(29, GPIO.FALLING, button_1, bouncetime=400)
    GPIO.add_event_detect(33, GPIO.FALLING, button_false, bouncetime=400)
    GPIO.add_event_detect(35, GPIO.FALLING, button_true, bouncetime=400)

	reading_thread = new Thread(target=read_w1_bus)
	reading_thread.start()

    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
