import os, sys, pathlib, shutil
from filequery import FileQuery


class FileOps(object):

    def __init__(self, db):
        self.db = db
        self.query = FileQuery(self.db)

        
    def get_file(self, file_id, dst, root=None, mount=None):
        item = self.query.get_item(file_id)
        file_path = self.query.get_folder(item['folder'])['fullpath']

        if not root:
            root = self.query.root_path(item['root'])
            if mount:
                mount = pathlib.Path(mount).resolve()
                if root[0] == '/':
                    root = root[1:]
                root = os.path.join(mount, root)
                
        if not os.path.exists(root):
            return f'Storage root not found:\n\t{root}'
        
        file_path = os.path.join(root, file_path)
        file_path = os.path.join(file_path, item['name'])
        dst = pathlib.Path(dst).resolve()
                
        if os.path.exists(file_path):
            shutil.copy2(file_path, dst)
            return 'OK'
        else:
            return f'File not found:\n\t{file_path}'
            
