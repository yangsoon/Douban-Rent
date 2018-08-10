from tornado.options import define, options
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import dbrent

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="debug Mode", type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r'/', dbrent.handlers),
        ]
        settings = dict(
            debug=options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
