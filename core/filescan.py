import os, sys, hashlib
from datetime import datetime
from util import *


class FileScan(object):
    
    def __init__(self, db):
        self.verbose = False
        self.root = None
        self.db = db


    def log(self, message):
        if self.verbose:
            print(message)
        

    def get_file_info(self, file_path):
        size = os.path.getsize(file_path)
        if size > (1024**3):
            self.log(f'Large file ({bytes_to_readable(size)}): {file_path.split("/")[-1:][0]}')
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
                
                parent_id = self.db.add_record('folders', {
                    'parent': parent_id,
                    'root': self.root_id,
                    'name': item,
                    'fullpath': folder_path
                })
            
            
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

        if self.db.record_exists('items', [
            {'field': 'root', 'value': self.root_id},
            {'field': 'folder', 'value': file_info['folder']},
            {'field': 'name', 'value': file_info['name']}
        ]):
            # we could check to update the file here?
            self.log(f'Skipping: {"/".join(path)}')
        else:
            self.log(f'New file: {"/".join(path)}')
            file_info['hash'] = get_file_hash(full_path)
            self.db.add_record('items', file_info)

            
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

        
    def add_root(self, name, root):
        self.root = root
        sql = "SELECT * FROM `roots` WHERE `path` = %s"
        existing = self.db.get_record(sql, (root, ))
        if existing:
            self.root_id = existing['id']
        else:
            self.root_id = self.db.add_record('roots', {'name': name, 'path': root})
        self.process_folder('')
