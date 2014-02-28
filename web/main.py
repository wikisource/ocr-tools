import tornado.httpserver
from tornado.web import RequestHandler, Application
import tornado.ioloop
from settings import settings
import utils
from parsedjvutext import image_from_book
import io

class MainHandler(RequestHandler):

    def get(self, page_number):
        areas, words = utils.gen_html("", page_number)
        self.render("index.html", page_number=page_number,
                    areas=areas, words=words)

class ImageHandler(RequestHandler):

    def get(self, page_number):
        im = image_from_book("../Villiers_de_L'Isle-Adam_-_Tribulat_Bonhomet,_1908.djvu", int(page_number))
        self.set_header('Content-Type', 'image/png')
        img_buff = io.BytesIO()
        im.save(img_buff, format="PNG")
        img_buff.seek(0)
        self.write(img_buff.read())
        self.finish()

application = Application([
    (r'/(\d+)/?', MainHandler),
    (r'/(\d+)\.png/?', ImageHandler)]
    , **settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print "Listening on 8888"
    tornado.ioloop.IOLoop.instance().start()
