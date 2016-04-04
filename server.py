from datetime import datetime
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import base64
import crypto
import json
import time


class MainHandler(RequestHandler):
    def get(self):
        cookie = self.get_cookie("user")
        if cookie:
            decrypted = crypto.decrypt(base64.b64decode(cookie))
            try:
                user_data = json.loads(decrypted)
                admin = " Admin" if user_data["is_admin"] else ""
                first_seen = datetime.fromtimestamp(user_data["first_seen"])
                self.write("Hello%s! I first saw you at: %s\n" %
                           (admin, first_seen))
                return
            except:
                pass

        # Generate a cookie for the user
        user_data = {
            "is_admin": False,
            "first_seen": int(time.time()),
        }
        cookie = base64.b64encode(crypto.encrypt(json.dumps(user_data)))
        self.set_cookie("user", cookie, path=None)
        self.write("Hello! I'll remember when I saw you.\n")


app = Application([
    (r"/", MainHandler),
])


if __name__ == "__main__":
    server = HTTPServer(app)
    server.bind(4555)
    server.start(0)  # Fork one process per cpu
    IOLoop.current().start()
