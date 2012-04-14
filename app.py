import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("debug", default=False, help="run in debug mode", type=bool)
define("port", default=8000, help="run on the given port", type=int)


class SockHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("socktest.html")

class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ajaxtest.html")

class AjaxEchoHandler(tornado.web.RequestHandler):
    def get(self):
        count =self.get_argument('count')
        data = {'count': int(count) + 1}
        self.write(data)

def app():
    app_settings = dict(
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      debug=options.debug,

    )
    return tornado.web.Application([
        (r"/socktest", SockHandler),
        (r"/ajaxtest", AjaxHandler),
        (r"/ajaxecho", AjaxEchoHandler),
    ], **app_settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app().listen(options.port)
    print "Running on port", options.port
    tornado.ioloop.IOLoop.instance().start()
