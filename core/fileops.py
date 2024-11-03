import os, sys, pathlib, shutil
from filequery import FileQuery


class FileOps(object):

    def __init__(self, db):
        self.db = db
        self.query = FileQuery(self.db)


    def get_file_path(self, file_id, root=None, mount=None):
        item = self.query.get_item(file_id)
        file_path = self.query.get_folder(item['folder'])['fullpath']

        if not root:
            root = self.query.root_path(item['root'])
            if mount:
                mount = pathlib.Path(mount).resolve()
                if root[0] == '/':
                    root = root[1:]
                root = os.path.join(mount, root)
                
        file_path = os.path.join(root, file_path)
        file_path = os.path.join(file_path, item['name'])
        return file_path
        
        
    def copy_file(self, file_id, dst, root=None, mount=None):
        file_path = self.get_file_path(file_id, root=root, mount=mount)
        dst = pathlib.Path(dst).resolve()

        if os.path.exists(dst) and os.path.isdir(dst):
            if os.path.exists(file_path):
                shutil.copy2(file_path, dst)
            else:
                return f'File not found:\n\t{file_path}'
        else:
            return f'Destination not found:\n\t{dst}'
            

    def merge(self, *folders, dst='', root=None, mount=None):
        if os.path.exists(dst) and os.path.isdir(dst):
            copy_errors = []
            files = {}
            for folder in folders:
                file_list = self.query.get_items(folder, as_dict=True)
                files = files | file_list # merge both dicts
     
            for key, item in files.items():
                file_path = self.get_file_path(item['id'], root=root, mount=mount)
                # if file is missing, we could try and 
                # find another file hash that matches?
                if os.path.exists(file_path):
                    shutil.copy2(file_path, dst)
                else:
                    copy_errors.append(file_path)

            if len(copy_errors) > 0:
                return '\n'.join(copy_errors)
        else:
            return f'Destination not found:\n\t{dst}'
            
