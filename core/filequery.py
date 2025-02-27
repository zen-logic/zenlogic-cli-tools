import os
from .util import get_file_hash


class FileQuery(object):

    def __init__(self, db):
        self.db = db
    

    def get_roots(self):
        items = []
        sql = "SELECT * FROM `roots` ORDER BY `name`"
        roots = self.db.get_records(sql, None)
        for root in roots:
            root = dict(root)
            if root['status'] == 'ok':
                if os.path.exists(root['path']):
                    root['status'] = 'online'
                else:
                    root['status'] = 'offline'
            items.append(root)
        return items


    def root_path(self, root_id):
        sql = "SELECT * FROM `roots` WHERE `id` = %s"
        root = self.db.get_record(sql, (root_id,))
        return root['path']
    

    def match_file(self, path):
        items = []
        if os.path.exists(path):
            h = get_file_hash(path)

            sql = """
            SELECT f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
            FROM `items` f1
                LEFT JOIN `folders` f2 ON f1.folder = f2.id
                LEFT JOIN `roots` r ON f1.root = r.id
            WHERE `hash` = %s
            """
            
            results = self.db.get_records(sql, (h, ))
            for item in results:
                items.append(dict(item))
        
        return items

    
    def find_hash(self, hash):
        items = []
        sql = """
        SELECT 'file' AS `type`, f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
        FROM `items` f1
            LEFT JOIN `folders` f2 ON f1.folder = f2.id
            LEFT JOIN `roots` r ON f1.root = r.id
        WHERE `hash` = %s
        """
        
        results = self.db.get_records(sql, (hash, ))
        for item in results:
            items.append(dict(item))
        
        return items
    

    def find_file_name(self, filename,
                       partial=False,
                       start=False,
                       end=False,
                       case_insensitive=False):
        escape = False
        items = []
        sql = """
        SELECT 'file' AS `type`, f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
        FROM `items` f1
            LEFT JOIN `folders` f2 ON f1.folder = f2.id
            LEFT JOIN `roots` r ON f1.root = r.id
        """
        if partial:
            sql += " WHERE f1.`name` LIKE %s"

            for char in ['_', '%']:
                if char in filename:
                    escape = '\\'
                    filename = filename.replace(char, f'\\{char}')

            if escape != False:
                escape = '\\'
                sql += f" ESCAPE '{escape}'"
                
            if start:
                filename = f'{filename}%'
            elif end:
                filename = f'%{filename}'
            else:
                filename = f'%{filename}%'
                
        else:
            sql += " WHERE f1.`name` = %s"

        if case_insensitive:
            sql += " COLLATE NOCASE"
        
        results = self.db.get_records(sql, (filename, ))
        for item in results:
            items.append(dict(item))
        
        return items
    

    def find_folder_name(self, foldername,
                         partial=False,
                         start=False,
                         end=False,
                         case_insensitive=False):
        items = []
        sql = """
        SELECT 'folder' AS `type`, f.*, r.name AS `rootname`, r.path AS `rootpath`
        FROM `folders` f
            LEFT JOIN `roots` r ON f.root = r.id
        """

        if partial:
            sql += " WHERE f.`name` LIKE %s"
            if start:
                foldername = f'{foldername}%'
            elif end:
                foldername = f'%{foldername}'
            else:
                foldername = f'%{foldername}%'
        else:
            sql += " WHERE f.`name` = %s"

        if case_insensitive:
            sql += " COLLATE NOCASE"

        sql += " ORDER BY `root`, `fullpath`"
        
        results = self.db.get_records(sql, (foldername, ))
        for item in results:
            items.append(dict(item))
        
        return items
        

    def find_path(self, path, end=False, start=False):
        items = []
        sql = """
        SELECT f.*, r.name AS `rootname`, r.path AS `rootpath`
        FROM `folders` f
            LEFT JOIN `roots` r ON f.root = r.id
        WHERE f.`fullpath` LIKE %s
        """
        sql += " ORDER BY `root`, `fullpath`"

        if end:
            param = f'%{path}'
        elif start:
            param = f'{path}%'
        else:
            param = f'%{path}%'
        
        results = self.db.get_records(sql, (param, ))
        for item in results:
            items.append(dict(item))
        
        return items

    
    def find_ext(self, ext, case_insensitive=False):
        items = []
        sql = """
        SELECT f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
        FROM `items` f1
            LEFT JOIN `folders` f2 ON f1.folder = f2.id
            LEFT JOIN `roots` r ON f1.root = r.id
        WHERE f1.`ext` = %s
        """
        if case_insensitive:
            sql += " COLLATE NOCASE"
        
        results = self.db.get_records(sql, (ext, ))
        for item in results:
            items.append(dict(item))
        
        return items
    
    
    def folder_hierarchy(self, folder_id, as_dict=False, key='path'):
        sql = """
        WITH RECURSIVE FolderHierarchy AS (
            SELECT *, name AS path
            FROM folders
            WHERE id=%s
            UNION ALL
            
            SELECT f.*, fh.path || '/' || f.name
            FROM folders f
            JOIN FolderHierarchy fh ON f.parent = fh.id
        )
         
        SELECT * FROM FolderHierarchy;
        """
        
        folders = self.db.get_records(sql, (folder_id,))
        if as_dict:
            items = {}
            for folder in folders:
                items[folder[key]] = dict(folder)
        else:
            items = []
            for folder in folders:
                items.append(dict(folder))
                
        return items
                

    def folder_compare(self, a, b, operation='difference'):
        """Compare two folder hierarchies (a and b).
        
        operations:
            a-not-b    : in a, not in b
            b-not-a    : in b, not in a
            difference : in either a or b but not in both
            both       : in both a and b
            union      : all from a and b
        """

        a = self.folder_hierarchy(a, as_dict=True)
        b = self.folder_hierarchy(b, as_dict=True)

        items = []
        
        if operation == 'a-not-b':
            filtered = set(a.keys()) - set(b.keys())
            items = list(map(lambda path: dict(a[path]), filtered))
            
        elif operation == 'b-not-a':
            filtered = set(b.keys()) - set(a.keys())
            items = list(map(lambda path: dict(b[path]), filtered))
            
        elif operation == 'difference':
            diff = set(a.keys()).symmetric_difference(set(b.keys()))
            for path in diff:
                if path in a:
                    items.append(dict(a[path]))
                else:
                    items.append(dict(b[path]))

        elif operation == 'both':
            intersection = set(a.keys()).intersection(set(b.keys()))
            for path in intersection:
                # path exists in both sets - take first item
                # and add second as a match
                item = dict(a[path])
                item['match'] = [b[path]['id']] # add as list to allow further matches
                items.append(item)
            
        elif operation == 'union':
            union = set(a.keys()).union(set(b.keys()))
            for path in union:
                # path might exist in either set - if it does,
                # add both references to returned item
                if path in a:
                    item = dict(a[path])
                    if path in b:
                        item['match'] = [b[path]['id']]
                    items.append(item)
                else:
                    item = dict(b[path])
                    if path in a:
                        item['match'] = [a[path]['id']]
                    items.append(item)

        return items
        

    def file_compare(self, a, b, operation='difference'):
        """Compare files in two folders (a and b).
        
        operations:
            a-not-b    : in a, not in b
            b-not-a    : in b, not in a
            difference : in either a or b but not in both
            both       : in both a and b
            union      : all from a and b
        """

        a = self.get_items(a, as_dict=True)
        b = self.get_items(b, as_dict=True)

        items = []
        
        if operation == 'a-not-b':
            filtered = set(a.keys()) - set(b.keys())
            items = list(map(lambda key: dict(a[key]), filtered))
            
        elif operation == 'b-not-a':
            filtered = set(b.keys()) - set(a.keys())
            items = list(map(lambda key: dict(b[key]), filtered))
            
        elif operation == 'difference':
            diff = set(a.keys()).symmetric_difference(set(b.keys()))
            for key in diff:
                if key in a:
                    items.append(dict(a[key]))
                else:
                    items.append(dict(b[key]))

        elif operation == 'both':
            intersection = set(a.keys()).intersection(set(b.keys()))
            for key in intersection:
                # hash exists in both sets - take first item
                # and add second as a match
                item = dict(a[key])
                item['match'] = [b[key]['id']] # add as list to allow further matches
                items.append(item)
            
        elif operation == 'union':
            union = set(a.keys()).union(set(b.keys()))
            for key in union:
                # hash might exist in either set - if it does,
                # add both references to returned item
                if key in a:
                    item = dict(a[key])
                    if key in b:
                        item['match'] = [b[key]['id']]
                    items.append(item)
                else:
                    item = dict(b[key])
                    if key in a:
                        item['match'] = [a[key]['id']]
                    items.append(item)

        return items


    def get_items(self, folder_id, as_dict=False):
        sql = """
        SELECT * FROM `items` WHERE `folder` = %s
        """
        results = self.db.get_records(sql, (folder_id, ))
        if as_dict:
            items = {}
            for item in results:
                items[item['hash']] = dict(item)
        else:
            items = []
            for item in results:
                items.append(dict(item))
        return items
    

    def get_folder(self, folder_id):
        sql = """
        SELECT 'folder' AS `type`, f.*, r.name AS `rootname`, r.path AS `rootpath`
        FROM `folders` f
            LEFT JOIN `roots` r ON f.root = r.id
        WHERE f.`id` = %s
        """
        item = self.db.get_record(sql, (folder_id, ))
        if item:
            return dict(item)
        else:
            return None


    def get_item(self, item_id):
        sql = """
            SELECT f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
            FROM `items` f1
                LEFT JOIN `folders` f2 ON f1.folder = f2.id
                LEFT JOIN `roots` r ON f1.root = r.id
            WHERE f1.`id` = %s
        """
        # sql = """
        # SELECT * FROM `items` WHERE `id` = %s
        # """
        item = self.db.get_record(sql, (item_id, ))
        if item:
            return dict(item)
        else:
            return None
        
    
    def get_root(self, root_id):
        items = []
        sql = "SELECT * FROM `folders` WHERE `root` = %s AND `parent` IS NULL ORDER BY `name`"
        folders = self.db.get_records(sql, (root_id,))
        for folder in folders:
            folder = dict(folder)
            folder['type'] = 'folder'
            folder['path'] = folder['fullpath']
            items.append(folder)
            
        sql = "SELECT * FROM `items` WHERE `root` = %s AND `folder` IS NULL ORDER BY `name`"
        files = self.db.get_records(sql, (root_id,))
        for item in files:
            item = dict(item)
            item['type'] = 'file'
            items.append(item);
            
        return items


    def get_folder_list(self, folder_id):
        items = []
        sql = "SELECT * FROM `folders` WHERE `parent` = %s"
        folders = self.db.get_records(sql, (folder_id,))
        for folder in folders:
            folder = dict(folder)
            folder['type'] = 'folder'
            folder['path'] = folder['fullpath']
            items.append(folder)
        
        sql = "SELECT * FROM `items` WHERE `folder` = %s"
        files = self.db.get_records(sql, (folder_id,))
        for item in files:
            item = dict(item)
            item['type'] = 'file'
            items.append(item)

        return items
    

    def get_tree(self, folder_id, depth=0, indent=4, files=False):
        hierarchy = self.folder_hierarchy(folder_id, as_dict=True, key='id')
        tree = []
        for key, item in hierarchy.items():
            if item['parent'] == None or item['parent'] not in hierarchy:
                tree.append(item)
            else:
                parent = hierarchy[item['parent']]
                if not 'children' in parent:
                    parent['children'] = []
                children = parent['children']
                children.append(item)

            if files:
                sql = "SELECT * FROM `items` WHERE `folder` = %s"
                files = self.db.get_records(sql, (item['id'],))
                for f in files:
                    if not 'children' in item:
                        item['children'] = []
                    children = item['children']
                    children.append(dict(f))
                
        return tree


    def get_stats(self):
        sql = """
        SELECT  (
            SELECT COUNT(*)
            FROM   `folders`
            ) AS `folders`,
            (
            SELECT COUNT(*)
            FROM   `items`
            ) AS `files`
        """
        stats = self.db.get_record(sql, None)
        return dict(stats)
    

    def get_path(self, folder_id):
        path = []
        sql = "SELECT * FROM `folders` WHERE `id` = %s"
        folder = self.db.get_record(sql, (folder_id,))
        path.append(dict(folder))

        while folder['parent'] != None:
            folder = self.db.get_record(sql, (folder['parent'],))
            path.append(dict(folder))

        sql = "SELECT * FROM `roots` WHERE `id` = %s"
        root = self.db.get_record(sql, (folder['root'],))
            
        path.append(dict(root))
        path.reverse()
        return path
    
