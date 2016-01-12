import os, logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options

define("debug", default=True, help="run in debug mode", type=bool)
define("port", default=8000, help="run on the given port", type=int)


class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ajaxtest.html")

class AjaxEchoHandler(tornado.web.RequestHandler):
    def get(self):
        count =self.get_argument('count')
        body =self.get_argument('body')
        data = {'count': int(count) + 1, 'body':body}
        self.write(data)

class WebsocketTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('websockettest.html')

class WebsocketTalkHandler(tornado.websocket.WebSocketHandler):
    waiters = []

    def open(self):
        WebsocketTalkHandler.waiters.append(self)

    def on_close(self):
        WebsocketTalkHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, message):
        #logging.info("sending message to %d waiters", len(cls.waiters))
        logging.info("%s" % message['count'])
        cls.waiters[0].write_message(message)
        # for waiter in cls.waiters:
        #     waiter.write_message(message)

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        parsed['count'] = int(parsed['count'])+1
        WebsocketTalkHandler.send_updates(parsed)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""<html>
        <a href=/ajaxtest>ajaxtest</a><br>
        <a href=/websockettest>websockettest</a><br>
        </html>""")


def app():
    app_settings = dict(
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      debug=options.debug,

    )
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/ajaxtest", AjaxHandler),
        (r"/ajaxecho", AjaxEchoHandler),
        (r"/websockettest", WebsocketTestHandler),
        (r"/websockettalk", WebsocketTalkHandler),

    ], **app_settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app().listen(options.port)
    print "Running on port", options.port
    tornado.ioloop.IOLoop.instance().start()
