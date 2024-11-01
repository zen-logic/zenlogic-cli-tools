import os
from util import get_file_hash


class FileQuery(object):

    def __init__(self, db):
        self.db = db
    

    def get_roots(self):
        items = []
        sql = "SELECT * FROM `roots`"
        roots = self.db.get_records(sql, None)
        for root in roots:
            items.append(dict(root))
        return items
    

    def match_file(self, path):
        items = []
        if os.path.exists(path):
            h = get_file_hash(path)

            sql = """
            SELECT f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
            FROM `items` f1
                JOIN `folders` f2 ON f1.folder = f2.id
                JOIN `roots` r ON f1.root = r.id
            WHERE `hash` = %s
            """
            
            results = self.db.get_records(sql, (h, ))
            for item in results:
                items.append(dict(item))
        
        return items

    
    def find_hash(self, hash):
        items = []
        sql = """
        SELECT f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
        FROM `items` f1
            JOIN `folders` f2 ON f1.folder = f2.id
            JOIN `roots` r ON f1.root = r.id
        WHERE `hash` = %s
        """
        
        results = self.db.get_records(sql, (hash, ))
        for item in results:
            items.append(dict(item))
        
        return items
    

    def find_file_name(self, filename, case_insensitive=False):
        items = []
        sql = """
        SELECT f1.*, f2.fullpath, r.name AS `rootname`, r.path AS `rootpath`
        FROM `items` f1
            JOIN `folders` f2 ON f1.folder = f2.id
            JOIN `roots` r ON f1.root = r.id
        WHERE f1.`name` = %s
        """
        if case_insensitive:
            sql += " COLLATE NOCASE"
        
        results = self.db.get_records(sql, (filename, ))
        for item in results:
            items.append(dict(item))
        
        return items
    

    def find_folder_name(self, foldername, case_insensitive=False):
        items = []
        sql = """
        SELECT f.*, r.name AS `rootname`, r.path AS `rootpath`
        FROM `folders` f
            JOIN `roots` r ON f.root = r.id
        WHERE f.`name` = %s
        """
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
            JOIN `roots` r ON f.root = r.id
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

    
    def folder_hierarchy(self, folder_id, as_dict=False):
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
                items[folder['path']] = folder['id']
        else:
            items = []
            for folder in folders:
                items.append(dict(folder))
                
        return items
                

    def folder_diff(self, a, b, all=False):
        a = self.folder_hierarchy(a, as_dict=True)
        b = self.folder_hierarchy(b, as_dict=True)

        if not all:
            # paths in a, not in b
            in_a = set(a.keys()) - set(b.keys())
            return list(map(lambda item: a[item], in_a))
        else:
            # paths in either a or b but not in both
            diff = set(a.keys()).symmetric_difference(set(b.keys()))
            items = []
            for item in diff:
                if item in a:
                    items.append(a[item])
                else:
                    items.append(b[item])
            return items


    def list(self, folder_id):
        items = []
        sql = """
        SELECT * FROM `items` WHERE `folder` = %s
        """
        results = self.db.get_records(sql, (folder_id, ))
        for item in results:
            items.append(dict(item))
        return items
    