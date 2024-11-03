import os, sys, pathlib, shutil
from filequery import FileQuery


class FileOps(object):

    def __init__(self, db):
        self.db = db
        self.query = FileQuery(self.db)


    def get_file_path(self, file_id, root=None, mount=None):
        item = self.query.get_item(file_id)
        if 'folder' in item:
            print(item['folder'])
            file_path = self.query.get_folder(item['folder'])['fullpath']
        else:
            file_path = ''

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
            

    def get_file_paths_from_folders(self, *folders, root=None, mount=None):
        paths = []
        files = {}
        for folder in folders:
            file_list = self.query.get_items(folder, as_dict=True)
            files = files | file_list # merge both dicts
 
        for key, item in files.items():
            file_path = self.get_file_path(item['id'], root=root, mount=mount)

            # if file is missing, try and find another matching file
            if not os.path.exists(file_path):
                alternatives = self.query.find_hash(item['hash'])
                for alt in alternatives:
                    file_path = self.get_file_path(alt['id'], root=root, mount=mount)
                    if os.path.exists(file_path):
                        break
                    
            paths.append(file_path)

        return paths

    
    def merge_folders(self, *folders, dst='./', root=None, mount=None):
        if os.path.exists(dst) and os.path.isdir(dst):
            copy_errors = []
            file_paths = self.get_file_paths_from_folders(*folders, root=root, mount=mount)
            for file_path in file_paths:
                if os.path.exists(file_path):
                    shutil.copy2(file_path, dst)
                else:
                    copy_errors.append(file_path)
            if len(copy_errors) > 0:
                return copy_errors
        else:
            return f'Destination not found:\n\t{dst}'
            

    def merge_folder_trees(self, *folders, dst='./', root=None, mount=None):
        copy_errors = []
        
        # get all folders to work on
        paths = {}
        for folder_id in folders:
            folder = self.query.get_folder(folder_id)
            base = folder['fullpath']
            tree = self.query.folder_hierarchy(folder_id)
            for item in tree:
                path = item['fullpath']
                path = path.replace(base, '')
                if not path in paths:
                    paths[path] = []
                paths[path].append(item)

        for path in paths:
            # create new folders as necessary
            dst_path = os.path.join(pathlib.Path(dst).resolve(), path)
            print(f'Creating folder: {dst_path}')
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)

            # get all the files to copy
            folder_ids = list(map(lambda item: item['id'], paths[path]))
            file_paths = self.get_file_paths_from_folders(*folder_ids, root=root, mount=mount)

            # copy all the files
            for file_path in file_paths:
                if os.path.exists(file_path):
                    print(f'Copying: {file_path}')
                    shutil.copy2(file_path, dst_path)
                else:
                    copy_errors.append(file_path)

        if len(copy_errors) > 0:
            return copy_errors
