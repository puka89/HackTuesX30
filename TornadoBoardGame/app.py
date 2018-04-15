import tornado.ioloop as ioloop
import tornado.web as web
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler as ws
from RPi import GPIO

GPIO.setmode(GPIO.BOARD)
clients = []

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

def gpio_setup_event_handlers():
    pass

def print_state(data):
    print(data)

def main():
    #setup gpios
    gpio_setup()
    #add gpio inerrupt handlers
    gpio_setup_event_handlers()
    GPIO.add_event_detect(36, GPIO.FALLING, print_state)
    GPIO.add_event_detect(38, GPIO.FALLING, print_state)
    GPIO.add_event_detect(40, GPIO.FALLING, print_state)
    GPIO.add_event_detect(31, GPIO.FALLING, print_state)
    GPIO.add_event_detect(15, GPIO.FALLING, print_state)
    GPIO.add_event_detect(23, GPIO.FALLING, print_state)
    GPIO.add_event_detect(21, GPIO.FALLING, print_state)
    GPIO.add_event_detect(19, GPIO.FALLING, print_state)
    GPIO.add_event_detect(5, GPIO.FALLING, print_state)
    GPIO.add_event_detect(18, GPIO.FALLING, print_state)
    GPIO.add_event_detect(16, GPIO.FALLING, print_state)
    GPIO.add_event_detect(12, GPIO.FALLING, print_state)
    GPIO.add_event_detect(11, GPIO.FALLING, print_state)
    GPIO.add_event_detect(13, GPIO.FALLING, print_state)
    GPIO.add_event_detect(22, GPIO.FALLING, print_state)
    GPIO.add_event_detect(32, GPIO.FALLING, print_state)    
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
