import json
import tornado.web
import logging
import generic_app

#import logging
#logging.basicConfig() 
#logger = logging.getLogger('baselogger')
#logger.warning("Debug output: %s", 'test params')


class BaseHandler(tornado.web.RequestHandler):
    # usually used to pass arguments. Cannot produce output or call methods like 'send_error'
    def initialize(self):
        with open('logs/requests.log', 'a') as wp:
            wp.write(str(self.request))
            wp.write('\n')
        self.title = "" 
        self.errors = []
        self.list0 = [] 
        self.list1 = [] 
        self.dict0 = {} 
        self.dict1 = {} 
        self.data0 = ''
        self.data1 = ''
        self.data2 = ''
        self.data3 = ''
        self.table = []
        self.table0 = []
        self.table1 = []
        self.plot_data0 = ""
        self.meta = ''

        self.navigation = self.create_navigation()

    def create_navigation(self): 
        endpoints = [ 
            "Funnel",
        ] 
        html  = '' 
        for endpoint in endpoints: 
            section = '''<li><a href="/{0}">{1}</a></li>\n'''\
                .format(endpoint.lower(),                                              endpoint.replace('_', ' '))
            html += section 
        return html 
        
    def get_html(self, template=None): 
        template_data = {
            'title': self.title + ' -- Woops!' if len(self.errors)>0 else self.title,
            'navigation': self.navigation, 
            'list0': self.errors if len(self.errors)>0 else self.list0, 
            'list1': self.list1, 
            'dict0': self.dict0, 
            'dict1': self.dict1,
            'data0': self.data0,
            'data1': self.data1,
            'data2': self.data2,
            'data3': self.data3,
            'table': self.table,
            'table0': self.table0,
            'table1':self.table1,
            'plot_data0': self.plot_data0, 
            'meta': self.meta,
        }  
        

        html_output = generic_app.master_layout.render(template_data)  
            
            
        return html_output 

    def get_text(self, data=[], delimiter='\n'): 
        if data==[]: 
            data=self.list0
        return delimiter.join(data)
        

    # shared by all handler subclasses. Always called and may produce output and/or redirect 
    def prepare(self):
        # Check if debug mode
        debug_mode = generic_app.get_env('debug')

        if debug_mode=='True':
            print("################### DEBUG MODE: %s ################### " % debug_mode)
            return

        # try:
        #     cookie = tornado.escape.json_decode(self.get_secure_cookie("smashboard_user") )
        # except TypeError:
        #     cookie = None
        #     print('failed to get cookie')
        #     self.redirect('/login')
        #     return
  
        # results = smashboard.get_dict_from_db('''
        #                             SELECT 
        #                                 email, admin, locked, firstname
        #                             FROM
        #                                 smashboard_users
        #                             WHERE
        #                                 email = %s AND firstname = %s
        #                                     AND lastname = %s
        #                                     AND admin = %s
        #                             ''', (cookie.get('email'), cookie.get('firstname'), cookie.get('lastname'), cookie.get('admin')))


        # if not results:
        #     self.redirect('/login')

        # elif results.get('locked') == 1:
        #     self.redirect('/locked_out')

        # elif results and results.get('firstname') == cookie.get('firstname') and results.get('email') == cookie.get('email'):
        #     pass