import generic_app 

class My404Handler(generic_app.BaseHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def get(self):
        self.set_status(404)
        self.title = 'This page is under development'
        self.write(self.get_html() )
