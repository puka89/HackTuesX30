import tornado.ioloop as ioloop
import tornado.web as web
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler as ws
from RPi import GPIO

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
    pass

def gpio_setup_event_handlers():
    pass

def main():
    #setup gpios
    gpio_setup()
    #add gpio inerrupt handlers
    gpio_setup_handlers()

    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
