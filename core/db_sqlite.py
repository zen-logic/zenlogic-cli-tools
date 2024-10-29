import sqlite3, datetime


def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()

def adapt_datetime_epoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())

def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.datetime.fromtimestamp(int(val))

sqlite3.register_converter("date", convert_date)
sqlite3.register_converter("datetime", convert_datetime)
sqlite3.register_converter("timestamp", convert_timestamp)


class Database(object):

    def __init__(self, db_file):
        self.con = None
        self.db_file = db_file

        
    def __del__(self):
        self.cleanup()


    def cleanup(self):
        if self.con != None:
            self.con.close()
            self.con = None


    def get_connection(self):
        if self.con == None:
            self.con = sqlite3.connect(self.db_file)
            self.con.row_factory = sqlite3.Row


    def run_sql_file(self, sql_file):
        with open(sql_file, 'r') as f:
            sql = f.read()
            
        self.get_connection()
        cur = self.con.cursor()
        cur.executescript(sql)
        self.con.commit()
        cur.close()
            

    def execute(self, sql, params):
        sql = sql.replace('%s', '?')
        self.get_connection()
        cur = self.con.cursor()
        if params != None:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        self.con.commit()
        cur.close()

        
    def get_match_sql(self, match):
        if type(match) == list:
            items = []
            for item in match:
                items.append(f"`{item['field']}` = ?")
            return ' AND '.join(items)
        else:
            return f"`{match['field']}` = ?"
            

    def get_match_values(self, match):
        if type(match) == list:
            items = []
            for item in match:
                items.append(item['value'])
            return tuple(items)
        else:
            return tuple([match['value']])


    def get_record(self, sql, params):
        sql = sql.replace('%s', '?')
        self.get_connection()
        cur = self.con.cursor()
        if params != None:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        record = cur.fetchone()
        cur.close()
        return record


    def get_records(self, sql, params):
        sql = sql.replace('%s', '?')
        self.get_connection()
        cur = self.con.cursor()
        if params != None:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        records = cur.fetchall()

        cur.close()
        return records


    def iterate_records(self, sql, params, callback):
        sql = sql.replace('%s', '?')
        self.get_connection()
        cur = self.con.cursor()
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
        sql = sql + ",".join(["?"] * len(data))
        sql = sql + ")"
    
        self.get_connection()
        cur = self.con.cursor()
    
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
            items.append("`%s`=%s" % (key, '?'))
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
        cur = self.con.cursor()
        cur.execute(sql, self.get_match_values(match))
        record = cur.fetchone()
        cur.close()
        return record != None
        

    def add_or_update(self, table_name, match, data):
        if self.record_exists(table_name, match):
            self.update_record(table_name, match, data)
        else:
            self.add_record(table_name, data)

    
        
