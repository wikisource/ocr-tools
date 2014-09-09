import tornado.httpserver
from tornado.web import RequestHandler, Application
import tornado.ioloop
from settings import settings
from utils.djvu_utils import image_from_book
from utils.wikisource import gen_html
import io

class MainHandler(RequestHandler):

    def get(self, page_number):
        orig_coords, orig_words, corr_words = \
                                              gen_html(self.settings["book"], int(page_number))
        self.render("index.html", page_number=page_number,
                    orig_coords=orig_coords,
                    orig_words=orig_words, corr_words=corr_words._elem)

class ImageHandler(RequestHandler):

    def get(self, page_number):
        im = image_from_book(self.settings["book"], int(page_number))
        self.set_header('Content-Type', 'image/jpg')
        img_buff = io.BytesIO()
        im.save(img_buff, format="JPEG")
        img_buff.seek(0)
        self.write(img_buff.read())
        self.finish()

def run():
    application = Application([
        (r'/(\d+)/?', MainHandler),
        (r'/(\d+)\.jpg/?', ImageHandler)], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print "Listening on 8888"
    tornado.ioloop.IOLoop.instance().start()
