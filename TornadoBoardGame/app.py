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

clients = []

dice_flag = 0
answer_flag = 0
start_game_flag = 0

playing = ["03172455d7ff", "0317243e28ff", "03172459f6ff", "0317243c31ff"]

queue = Queue()

gpio_fields = {
	"36" : 1,
	"38" : 2,
	"40" : 3,
	"31" : 4,
	"15" : 5,
	"23" : 6,
	"21" : 7,
	"19" : 8,
	"5" : 9,
	"18" : 10,
	"16" : 11,
	"12" : 12,
	"11" : 13,
	"13" : 14,
	"22" : 15,
	"32" : 16
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

buttons_gpio = {
	"1" : 29,
	"2" : 33,
	"3" : 35
}

def make_app():
    return web.Application([
        (r"/", GameHandler),
        (r"/index", GameWebSocket),
    ])

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

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

def read_w1_bus():
	sensor_ids = []
	sensors_temp = DS18B20.get_all_sensors()
	for sensor in sensors_temp:
	    sensor_ids.append(sensor.get_id())

	return sensor_ids

def blocking_debounce():
	low_count = 0
	high_count = 0

	while !queue.empty():
		pin = queue.get_nowait()

	    while True:
	        if high_count == 3:
				pulling_event(pin)
				GPIO.add_event_detect(pin, GPIO.BOTH, handle_gpio)
				low_count = 0
				high_count = 0
				break

			if low_count == 3:
				putting_event(pin)
				GPIO.add_event_detect(pin, GPIO.BOTH, handle_gpio)
				low_count = 0
				high_count = 0
				break

	        if GPIO.input(event) == GPIO.LOW:
	            low_count += 1
	        else:
	            high_count += 1

	        time.sleep(0.1)

def handle_gpio(pin):
	GPIO.remove_event_detect(pin)
	queue.put_nowait(pin)

def pulling_event(pin):
	time.sleep(0.7)
	current = read_w1_bus()
	removed_pawn_id = diff(playing, current)
	positions[gpio_fields[pin]] = ""

def putting_event(pin):
	time.sleep(0.7)
	positions[gpio_fields[pin]] = removed_pawn_id

	if fields_status[int(gpio_fields[pin])] == 'red':
		prompt_question(sensors_dict[removed_pawn_id])

	removed_pawn_id = ""

def prompt_question(player):
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
	GPIO.add_event_detect(33, GPIO.BOTH, button_false)
    GPIO.add_event_detect(35, GPIO.BOTH, button_true)
	GPIO.remove_event_detect(29)

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

def gpio_events():
	GPIO.add_event_detect(36, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(38, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(40, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(31, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(15, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(23, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(21, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(19, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(5, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(18, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(16, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(12, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(11, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(13, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(22, GPIO.BOTH, handle_gpio)
    GPIO.add_event_detect(32, GPIO.BOTH, handle_gpio)
	GPIO.add_event_detect(29, GPIO.BOTH, button_1)

def init_players():
	pass

def main():
    gpio_setup()
	gpio_events()
	init_players()

	blocking_debounce_thread = new Thread(target=blocking_debounce)
	blocking_debounce_thread.start()

    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
