from generic_app import *


creds = configparser.ConfigParser()
creds.read('./.databases.conf')



# class posgres_connect:

#     def __init__(self, database):
#         self.database = database
#         dbname = creds.get(database, 'dbname')
#         user = creds.get(database, 'user')
#         password = creds.get(database, 'password')
#         host = creds.get(database, 'host')
#         port = creds.get(database, 'port')
#         self.connection = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s' connect_timeout=0.00001" % (dbname, user, password, host, port))
#         self.cursor = self.connection.cursor(cursor_factory=DictCursor)
#         print('db connection opened')

#     def fetchall_dict(self, query, vars=None):
#         try:
#             self.cursor.execute(query, vars)
#             return self.cursor.fetchall()
#         except psycopg2.OperationalError as e:
#             print(str(e))
#             return



#     def close(self):
#         self.cursor.close()
#         self.connection.close()
#         print('db connection closed')

#     def toString(self):
#             print("I'm a database connection object to " + self.database + ", look at me go \n")


class mysql_connect:

    def __init__(self):
        self.connection = MySQLdb.connect(creds.get('mysql', 'host'),
                    creds.get('mysql', 'user'),
                    creds.get('mysql', 'password'),
                    creds.get('mysql', 'db'))

        print('mysql db connection open')

         
    def get_items_from_db(self, query, params={}, include_columns=False): 
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall() 

        results = [] 

        for row in data:
            line = list(row)
            results.append(line)

        columns = [i[0] for i in cursor.description]
        if include_columns == True:
            results.insert(0, columns)
            return results  
        else: 
            return results


    def get_dict_from_db(self, query, params={}): 
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        return cursor.fetchone() 


    def get_dicts_from_db(self, query, params={}):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute(query, params)
        
        results = [] 
        for item in cursor.fetchall(): 
            results.append(item) 
        
        return results

    def update_db(query, params={}): 
        return insert_item_into_db(query, params)         
    

    def insert_item_into_db(self, query, params={}): 
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        # try: 
        #     db.commit() 
        # except MySQL.IntegrityError as e: 
        #     print(e)
            
    

    def close(self):
        self.connection.close()
        print('mysqldb connection closed')

