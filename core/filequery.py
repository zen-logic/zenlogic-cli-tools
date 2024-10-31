import os
from core.util import get_file_hash


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
        
