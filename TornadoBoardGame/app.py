import tornado.ioloop as ioloop
import tornado.web as web
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler as ws
from RPi import GPIO
from time import sleep
from threading import Thread

GPIO.setmode(GPIO.BOARD)
clients = []
sensor_ids = {
	"03172455d7ff" : "red",
	"0317243e28ff" : "black",
	"03172459f6ff" : "white",
	"0317243c31ff" : "yellow"
}

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
	sensors = DS18B20.get_all_sensors()
	for sensor in sensors:
	    sensor_ids.append(sensor.get_id())
	up_sensor
	time.sleep(.4)

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def print_state(data):
    time.sleep(1.5)
    print(data)

def button_1(data):
    print("you started")

def button_false(data):
    print("you said false")

def button_true (data):
    print("you said true")

def main():
    #setup gpios
    gpio_setup()
    #add gpio inerrupt handlers
    gpio_setup_event_handlers()
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

    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
