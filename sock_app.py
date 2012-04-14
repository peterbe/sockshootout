import tornado.options
import tornado.escape
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection
from tornado.options import define, options

define("debug", default=False, help="run in debug mode", type=bool)
define("port", default=9999, help="run on the given port", type=int)

class EchoConnection(SockJSConnection):
    def on_message(self, msg):
        data = tornado.escape.json_decode(msg)
        #print "Incoming", repr(data)
        data['count'] += 1
        self.send(data)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    EchoRouter = SockJSRouter(EchoConnection, '/echo')
    app_settings = dict(
      debug=options.debug
    )
    app = web.Application(EchoRouter.urls, **app_settings)
    app.listen(options.port)
    print "Running sock app on port", options.port
    ioloop.IOLoop.instance().start()
