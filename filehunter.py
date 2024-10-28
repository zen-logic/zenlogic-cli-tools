import os, sys, hashlib
from datetime import datetime
import core.db


db_config = {
    "database": "",
    "user": "",
    "password": "",
    "host": ""
}


class FileHunter(object):
    
    def __init__(self):
        self.verbose = False
        self.root = None
        self.db = core.db.Database(db_config)


    def get_file_info(self, file_path):
        size = os.path.getsize(file_path)
        if self.verbose and size > (1024**3):
            print(f'Large file (>1Gb): {file_path.split("/")[-1:]}')
            
        mtime = datetime.fromtimestamp(os.path.getctime(file_path))
        ctime = datetime.fromtimestamp(os.path.os.stat(file_path).st_birthtime)
        dummy, ext = os.path.splitext(file_path)
        with open(file_path, 'rb', buffering=0) as f:
            digest = hashlib.file_digest(f, 'md5').hexdigest()

        return {
            'hash': digest,
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
                if self.verbose:
                    print(f'New folder: {folder_path}')
                
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
            if self.verbose:
                print(f'Skipping: {"/".join(path)}')
        else:
            if self.verbose:
                print(f'New file: {"/".join(path)}')
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
            return
                
        
    def add_root(self, name, root):
        self.root = root
        sql = "SELECT * FROM `roots` WHERE `path` = %s"
        existing = self.db.get_record(sql, (root, ))
        if existing:
            self.root_id = existing['id']
        else:
            self.root_id = self.db.add_record('roots', {'name': name, 'path': root})
        self.process_folder('')
    
    
if __name__ == '__main__':
    
    fh = FileHunter()
    fh.verbose = True
    fh.add_root(
        'Toshiba 3Tb 3',
        '/Users/Shared/Mount/kuro/Volumes/Toshiba 3Tb 3/'
    )

    
