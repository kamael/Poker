import tornado.ioloop
import tornado.web
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./template/index.html")

class IcoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./a.ico")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/favicon.ico", IcoHandler),
    ], **settings)



if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

