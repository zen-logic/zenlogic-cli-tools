import os, sys, pathlib, json
from .db_sqlite import Database


def home_dir():
    return pathlib.Path.home().resolve()

def script_dir():
    return pathlib.Path(__file__).parent.resolve()

def data_dir():
    path = home_dir()
    path = os.path.join(path, '.zenlogic')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


class BaseCLI(object):
    
    def __init__(self, args):
        self.args = args
        self.setup()
        self.run()


    def run(self):
        if hasattr(self, self.args.command):
            getattr(self, self.args.command)()
        
            
    def setup(self):
        if self.args.database:
            db_file = self.args.database
        else:
            db_file = os.path.join(data_dir(), 'fh.db')
        self.db = Database(db_file)

        if not os.path.exists(db_file):
            blank = os.path.join(script_dir(), 'blank.sql')
            self.db.run_sql_file(blank)
