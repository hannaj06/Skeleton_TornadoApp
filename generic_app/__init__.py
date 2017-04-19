import redis 
import configparser
import MySQLdb
import _mysql
import logging
import tornado
from generic_app.base import BaseHandler
from generic_app.weberrors import My404Handler
from generic_app.main import * 
from generic_app.db_connect import mysql_connect
from string import Template
from jinja2 import Environment, FileSystemLoader, Template



logging.basicConfig()
logger = logging.getLogger('baselogger')
logger.warning("Debug output: %s", 'test params')

        
templateLoader = FileSystemLoader( searchpath = "templates/" )
templateEnv = Environment( loader = templateLoader)
master_layout = templateEnv.get_template("master.html")
login_layout = templateEnv.get_template('login.html')
locked_layout = templateEnv.get_template('locked_out.html')

### DON"T LIKE THIS> RETURNS STRING WHEN KEY, DICT WHEN ALL #####
def get_env(key): 
    env = configparser.ConfigParser() 
    env.read('./.env') 
    
    d = dict(env._sections['env'])
    if key=='ALL': 
        return d
    else: 
        return d.get(key, None) 

def get_env_dict(): 
    env = configparser.ConfigParser()
    env.read('./.env')
    return dict(env._sections['env'])

def get_cursor(cur_type=None): 
    creds = configparser.ConfigParser()
    creds.read('./.databases.conf')

    db = MySQLdb.connect(creds.get('mysql', 'host'),
                creds.get('mysql', 'user'),
                creds.get('mysql', 'password'),
                creds.get('mysql', 'db'),
        )
    if cur_type == None: 
        cur = db.cursor()
    elif cur_type == 'dict': 
        cur = db.cursor(MySQLdb.cursors.DictCursor)
    return cur 
     
def get_items_from_db(query, params={}, include_columns=False): 
    cur = get_cursor()
    cur.execute(query, params)
    data = cur.fetchall() 

    results = [] 
    for row in data:
        line = list(row)
        results.append(line)

    columns = [i[0] for i in cur.description]
    if include_columns == True: 
        return results, columns  
    else: 
        return results

def get_dict_from_db(query, params={}): 
    cur = get_cursor(cur_type='dict')
    cur.execute(query, params) 
    return cur.fetchone() 

def get_dicts_from_db(query, params={}): 
    cur = get_cursor(cur_type='dict')
    cur.execute(query, params) 
    
    results = [] 
    for item in cur.fetchall(): 
        results.append(item) 
    return results     

def get_api_key(service): 
    creds = configparser.ConfigParser()
    creds.read('./.databases.conf')
    return creds.get(service, 'api_key') 

def update_db(query, params={}): 
    return insert_item_into_db(query, params) 

def insert_item_into_db(query, params={}): 
    creds = configparser.ConfigParser()
    creds.read('./.databases.conf')

    db = MySQLdb.connect(creds.get('mysql', 'host'),
                creds.get('mysql', 'user'),
                creds.get('mysql', 'password'),
                creds.get('mysql', 'db'),
        )
    cur = db.cursor()
    cur.execute(query, params)
    try: 
        db.commit() 
    except MySQL.IntegrityError as e: 
        print(e)
        logging.warn("Failed to insert or delete from database")

def get_items_from_file(db): 
    items = []
    try: 
        with open('./databases/{db}.csv'.format(db=db), 'r') as rp:
            for line in rp.readlines():
                line = line.split('\t')
                items.append(line)    
    except IOError as e: 
        raise e 
    return items 
