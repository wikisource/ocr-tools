import tornado.httpserver
from tornado.web import RequestHandler, Application
import tornado.ioloop
from settings import settings
import utils


class MainHandler(RequestHandler):

    def get(self, page_number):
        areas, words = utils.gen_html("", page_number)
        self.render("index.html", page_number=page_number,
                    areas=areas, words=words)


application = Application([
    (r'/(\d+)/?', MainHandler)
], **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print "Listening on 8888"
    tornado.ioloop.IOLoop.instance().start()
