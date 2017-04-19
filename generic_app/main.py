import generic_app
import json

class MainHandler(generic_app.BaseHandler):
    def get(self):
        self.data0 = '''<div class="jumbotron"><h1>Dashboard</h1>
        				<p>Welcome!</p></div>'''
        self.write(self.get_html() )

class LoginHandler(generic_app.BaseHandler):
    def prepare(self):
        pass

    def get(self):
        self.write(smashboard.login_layout.render())

    def post(self):
        pass

class LockoutHandler(generic_app.BaseHandler):
    def prepare(self):
        pass

    def get(self):
        self.write(smashboard.locked_layout.render())