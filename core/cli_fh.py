import os, sys, pathlib, json
from cli_base import BaseCLI
from filescan import FileScan
from filequery import FileQuery


class CLI(BaseCLI):
    
    def __init__(self, args):
        super().__init__(args)

            
    def setup(self):
        super().setup()
        self.fmt = self.args.output
        self.fields = self.args.fields
        self.query = FileQuery(self.db)
        self.scanner = FileScan(self.db)
        

    def output(self, data):
        out = []
        if self.fields == None:
            # output all fields in whatever format is selected
            if self.fmt == 'json':
                print(json.dumps(data))
            elif self.fmt == 'table':
                fields = data.keys()
                for field in fields:
                    if field in data:
                        out.append(str(data[field]))
                    else:
                        out.append(f'missing field: {field}')
                print('\t'.join(out))
        else:
            # output selected fields in whatever format is selected
            fields = self.fields.split(',')
            if self.fmt == 'json':
                out = {}
                for field in fields:
                    if field in data:
                        out[field] = data[field]
                print(json.dumps(out))
            elif self.fmt == 'table':
                for field in fields:
                    if field in data:
                        out.append(str(data[field]))
                    else:
                        out.append(f'missing field: {field}')
                print('\t'.join(out))


    def scan(self):
        self.scanner.verbose = True
        self.scanner.add_root(self.args.name, self.args.path)
        self.scanner.process_folder('')

        
    def match(self):
        for item in self.query.match_file(self.args.filename):
            self.output(item)

            
    def find(self):
        t = self.args.type
        if t == 'file':
            for item in self.query.find_file_name(
                    self.args.item,
                    partial=self.args.partial,
                    start=self.args.start,
                    end=self.args.end,
                    case_insensitive=True):
                self.output(item)
        elif t == 'folder':
            for item in self.query.find_folder_name(
                    self.args.item,
                    partial=self.args.partial,
                    start=self.args.start,
                    end=self.args.end,
                    case_insensitive=True):
                self.output(item)
        elif t == 'ext':
            for item in self.query.find_ext(self.args.item, case_insensitive=True):
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


    def compare(self):
        t = self.args.type
        if t == 'folders':
            for folder in self.query.folder_compare(
                    self.args.a,
                    self.args.b,
                    self.args.operation
            ):
                self.output(folder)
        elif t == 'files':
            for item in self.query.file_compare(
                    self.args.a,
                    self.args.b,
                    self.args.operation
            ):
                self.output(item)
                

    def list(self):
        for item in self.query.get_items(self.args.item):
            self.output(item)


    def items(self):
        for item in self.query.get_folder_list(self.args.item):
            self.output(item)
            
                
    def roots(self):
        for root in self.query.get_roots():
            print(str(root['id']).rjust(5), root['name'].ljust(20), root['path'])


    def root(self):
        for item in self.query.get_root(self.args.item):
            self.output(item)
            
            
    def get(self):
        item = None
        t = self.args.type
        if t == 'file':
            item = self.query.get_item(self.args.id)
        elif t == 'folder':
            item = self.query.get_folder(self.args.id)
        if item:
            self.output(item)


    def tree(self):
        
        def print_node(node, depth=0, indent=2):
            print(f"{str(node['id']).rjust(8)}  {' ' * depth * indent}{node['name']}")
            if node.get('children',False):
                for child in node['children']:
                    print_node(child, depth=depth+1)
                    
        tree = self.query.get_tree(self.args.folder, files=self.args.files)

        if self.fmt == 'json':
            print(json.dumps(tree))
        else:
            for node in tree:
                print_node(node)
        
        

            
