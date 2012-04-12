import tornado.options
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection
from tornado.options import define, options

define("debug", default=False, help="run in debug mode", type=bool)
define("port", default=9999, help="run on the given port", type=int)

class EchoConnection(SockJSConnection):
    def on_message(self, msg):
        #print "Incoming", repr(msg)
        self.send(msg.upper())

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
