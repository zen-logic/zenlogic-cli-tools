import os, sys, pathlib, json
from filescan import FileScan
from filequery import FileQuery
from fileops import FileOps
from db_sqlite import Database


def home_dir():
    return pathlib.Path.home().resolve()

def script_dir():
    return pathlib.Path(__file__).parent.resolve()


class CLI(object):
    
    def __init__(self, args):
        self.args = args
        self.setup()
        db_file = 'test.db'
        db_file = os.path.join(script_dir(), db_file)
        self.db = Database(db_file)
        self.query = FileQuery(self.db)
        self.scan = FileScan(self.db)
        self.ops = FileOps(self.db)
        self.scan.verbose = True
        if not os.path.exists(db_file):
            blank = os.path.join(script_dir(), 'blank.sql')
            self.db.run_sql_file(blank)
            
        if hasattr(self, args.command):
            getattr(self, args.command)()

            
    def setup(self):
        self.fmt = self.args.output
        self.fields = self.args.fields
        

    def output(self, data):
        if self.fmt == 'json':
            print(json.dumps(data))
        elif self.fmt == 'fields':
            out = []
            if self.fields == None:
                # show all fields
                fields = data.keys()
            else:
                # only selected fields
                fields = self.fields.split(',')
                
            for field in fields:
                if field in data:
                    out.append(str(data[field]))
                else:
                    out.append(f'missing field: {field}')
            print(' | '.join(out))
        else:
            print('unrecognised format')

            
    def match(self):
        for item in self.query.match_file(self.args.filename):
            self.output(item)

            
    def find(self):
        t = self.args.type
        if t == 'file':
            for item in self.query.find_file_name(self.args.item, case_insensitive=True):
                self.output(item)
        elif t == 'folder':
            for item in self.query.find_folder_name(self.args.item, case_insensitive=True):
                self.output(item)
        elif t == 'hash':
            for item in self.query.find_hash(self.args.item):
                self.output(item)
        elif t == 'path':
            items = self.query.find_path(self.args.item,
                                         start=self.args.start,
                                         end=self.args.end)
            for item in items:
                self.output(item)
            
    
    def hierarchy(self):
        for folder in self.query.folder_hierarchy(self.args.id):
            self.output(folder)


    def diff(self):
        for folder in self.query.folder_diff(self.args.a,
                                             self.args.b,
                                             all=self.args.all):
            self.output(folder)


    def list(self):
        if self.args.item == 'roots':
            for root in self.query.get_roots():
                print(str(root['id']).rjust(5), root['name'].ljust(20), root['path'])
        else:
            for item in self.query.list(self.args.item):
                self.output(item)
