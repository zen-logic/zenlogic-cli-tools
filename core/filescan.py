import os, sys, hashlib
from datetime import datetime
from .util import *


class FileScan(object):
    
    def __init__(self, db, update=None):
        self.update = update
        self.verbose = False
        self.root = None
        self.db = db
        self.skip_count = 0
        self.file_count = 0
        self.folder_count = 0
        self.info = ''
        

    def log(self, message):
        if self.verbose:
            print(message)


    def notify(self, immediate=False):
        if self.update:
            data = {
                "info": {
                    "detail": self.info,
                    "stats": [
                        {"label": "Skipped", "value": self.skip_count},
                        {"label": "Files", "value": self.file_count},
                        {"label": "Folders", "value": self.folder_count}
                    ]
                }
            }
            self.update(data, immediate=immediate)
            

    def get_file_info(self, file_path):
        size = os.path.getsize(file_path)
        if size > (100 * (1024 * 1024)):
            self.log(f'Large file ({bytes_to_readable(size)}): {file_path.split("/")[-1:][0]}')
            self.info = f'Large file ({bytes_to_readable(size)}): {file_path.split("/")[-1:][0]}'
            self.notify(immediate=True)

        mtime = datetime.fromtimestamp(os.path.getctime(file_path))
        ctime = datetime.fromtimestamp(os.path.os.stat(file_path).st_birthtime)
        dummy, ext = os.path.splitext(file_path)
        return {
            'size': size,
            'created': ctime,
            'modified': mtime,
            'ext': ext[1:]
        }


    def add_folder(self, path):
        if path.endswith('/'): path = path[:-1]
        parent_id = None
        items = path.split('/')
        for idx, item in enumerate(items):
            folder_path = '/'.join(items[:idx+1])
            sql = "SELECT * FROM `folders` WHERE `fullpath` = %s AND `root` = %s"
            folder = self.db.get_record(sql, (folder_path, self.root_id))
            if folder:
                parent_id = folder['id']
            else:
                self.log(f'New folder: {folder_path}')
                self.info = f'New folder: {item}'
                
                parent_id = self.db.add_record('folders', {
                    'parent': parent_id,
                    'root': self.root_id,
                    'name': item,
                    'fullpath': folder_path
                })
            self.folder_count += 1
        self.notify()
            
            
    def add_file(self, path):
        full_path = os.path.join(self.root, path)
        file_info = self.get_file_info(full_path)
        path = path.split('/')
        file_info['name'] = path[-1:][0]
        folder_path = path[:-1]
        sql = "SELECT * FROM `folders` WHERE `fullpath` = %s AND `root` = %s"
        folder = self.db.get_record(sql, ('/'.join(folder_path), self.root_id))
        if folder:
            file_info['folder'] = folder['id']
        else:
            file_info['folder'] = None
        file_info['root'] = self.root_id

        if file_info['folder']:
            sql = "SELECT * FROM `items` WHERE `root` = %s AND `folder` = %s AND `name` = %s"
            existing = self.db.get_record(sql, (self.root_id, file_info['folder'], file_info['name']))
        else:
            sql = "SELECT * FROM `items` WHERE `root` = %s AND `folder` IS NULL AND `name` = %s"
            existing = self.db.get_record(sql, (self.root_id, file_info['name']))

        if existing:
            dt = datetime.fromtimestamp(existing['modified'])
            if dt == file_info['modified']:
                self.log(f'Skipping: {"/".join(path)}')
                self.info = f'Skipping: {file_info['name']}'
                self.skip_count += 1
            else:
                self.log(f'Modified file: {"/".join(path)}')
                file_info['hash'] = get_file_hash(full_path)
                self.info = f'Modified file: {file_info['name']}'
                self.db.update_record('items', {'field': 'id', 'value': existing['id']}, file_info)
                self.file_count += 1
        else:
            self.log(f'New file: {"/".join(path)}')
            file_info['hash'] = get_file_hash(full_path)
            self.info = f'New file: {file_info['name']}'
            self.db.add_record('items', file_info)
            self.file_count += 1
            
        self.notify()

            
    def process_folder(self, path):
        full_path = os.path.join(self.root, path)
        try:
            for item in os.listdir(full_path):
                current = os.path.join(full_path, item)
                item_path = os.path.join(path, item)
                if os.path.isdir(current) and not os.path.islink(current):
                    self.add_folder(item_path)
                    self.process_folder(item_path)
                elif os.path.isfile(current):
                    self.add_file(item_path)
        except PermissionError:
            self.log(f'Permission error: {full_path}')
            self.info = f'Permission error: {full_path}'

            
    def add_root(self, name, root):
        self.root = root
        sql = "SELECT * FROM `roots` WHERE `path` = %s"
        existing = self.db.get_record(sql, (root, ))
        if existing:
            self.root_id = existing['id']
        else:
            self.root_id = self.db.add_record('roots', {'name': name, 'path': root})
