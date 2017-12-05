import tornado.ioloop
import os
import tornado.web
import generic_app

def make_app():
    
    settings = {
    "cookie_secret": "3W5E8kMmG46kF2S69xVdt2EynCWZy3NZ",
    "login_url": "/login",
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    #'default_handler_class': generic_app.My404Handler, 
    'debug': True,
    'compiled_templates_cache': False,
    }

    return tornado.web.Application(
        [
            (r"/", generic_app.MainHandler),
            (r"/login", generic_app.LoginHandler),
            (r"/locked_out", generic_app.LockoutHandler),

        ], 
        **settings 
    )

if __name__ == "__main__":
    app = make_app()
    port = 8888
    app.listen(port)
    line = '\n\n==========================================\n\n'
    print('{0}Now running on 127.0.0.1:{1}{0}'.format(line, port))
    tornado.ioloop.IOLoop.current().start()
