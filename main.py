from tornado.options import define, options
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload
import motor.motor_tornado
import dbrent.handlers
from spider.config import mongo

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="debug Mode", type=bool)

db = motor.motor_tornado.MotorClient(mongo['host'], mongo['port']).douban


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/placelists', dbrent.handlers.PlaceListsHander),
            (r'/getrent', dbrent.handlers.RentInfoHandler),
            (r'/getdetail', dbrent.handlers.RentDetailHandler),
            (r'/filterrent', dbrent.handlers.RentFilterHandler)
        ]
        settings = dict(
            debug=options.debug,
            db=db
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
