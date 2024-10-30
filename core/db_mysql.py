import mysql.connector

class Database(object):

    transaction = False

    def __init__(self, config):
        self.con = None
        self.config = config


    def __del__(self):
        self.cleanup()


    def cleanup(self):
        if self.con != None:
            self.con.close()
            self.con = None
    

    def get_connection(self):
        if self.con == None:
            self.con = mysql.connector.connect(
                **self.config,
                auth_plugin='mysql_native_password'
            )
        if not self.con.is_connected():
            print ('MySQL not connected, retrying...')
            self.con.reconnect(attempts=3, delay=5)


    def get_match_sql(self, match):
        if type(match) == list:
            items = []
            for item in match:
                items.append("`%s` = %s" % (item['field'], '%s'))
            return ' AND '.join(items)
        else:
            return "`%s` = %s" % (match['field'], '%s')
            

    def get_match_values(self, match):
        if type(match) == list:
            items = []
            for item in match:
                items.append(item['value'])
            return tuple(items)
        else:
            return tuple([match['value']])

        
    def execute(self, sql, params):
        self.get_connection()
        cur = self.con.cursor()
        cur.execute(sql, params)
        self.con.commit()
        cur.close()


    def get_record(self, sql, params):
        self.get_connection()
        # need to set buffered=True to get a successful fetchone read
        cur = self.con.cursor(dictionary=True, buffered=True)
        cur.execute(sql, params)
        record = cur.fetchone()
        cur.close()
        return record


    def get_records(self, sql, params):
        self.get_connection()
        cur = self.con.cursor(dictionary=True)
        if params != None:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        records = cur.fetchall()

        cur.close()
        return records
        
    
    def iterate_records(self, sql, params, callback):
        self.get_connection()
        cur = self.con.cursor(dictionary=True)
        if params != None:
            cur.execute(sql, params)
        else:
            cur.execute(sql)

        while True:
            record = cur.fetchone()
            if record == None:
                break
            callback(record)
            
        cur.close()
    
        
    def add_record(self, table_name, data):

        sql = "INSERT INTO `%s` (" % (table_name)
        sql = sql + ",".join(["`%s`"] * len(data))
        sql = sql % tuple(data.keys())
    
        sql = sql + ") VALUES ("
        sql = sql + ",".join(["%s"] * len(data))
        sql = sql + ")"
    
        self.get_connection()
        cur = self.con.cursor(buffered=True)
    
        params = tuple(data.values())
    
        cur.execute(sql, params)
        id = cur.lastrowid
        self.con.commit()
        cur.close()
    
        return id



    def update_record(self, table_name, match, data):
        sql = "UPDATE `%s` SET " % (table_name)
    
        items = []
        for key in data.keys():
            items.append("`%s`=%s" % (key, '%s'))
        sql = sql + ','.join(items)
    
        sql = sql + " WHERE "
        sql = sql + self.get_match_sql(match)
    
        self.get_connection()
        cur = self.con.cursor()
    
        params = tuple(data.values()) + self.get_match_values(match)
    
        cur.execute(sql, params)
        self.con.commit()
        cur.close()


    def delete_records(self, table_name, match):
        sql = "DELETE FROM `%s` " % (table_name)
    
        sql = sql + " WHERE "
        sql = sql + self.get_match_sql(match)
    
        self.get_connection()
        cur = self.con.cursor()
    
        cur.execute(sql, self.get_match_values(match))
        self.con.commit()
        cur.close()


    def record_exists(self, table_name, match):
        sql = "SELECT * FROM `%s`" % (table_name)
        sql = sql + " WHERE "
        sql = sql + self.get_match_sql(match)

        self.get_connection()
        self.con.commit()
        # need to set buffered=True to get a successful fetchone read
        cur = self.con.cursor(dictionary=True, buffered=True)
        cur.execute(sql, self.get_match_values(match))
        record = cur.fetchone()
        cur.close()
        return record != None


    def add_or_update(self, table_name, match, data):
        if self.record_exists(table_name, match):
            self.update_record(table_name, match, data)
        else:
            self.add_record(table_name, data)
