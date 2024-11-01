import os, sys, pathlib, json
from filescan import FileScan
from filequery import FileQuery


class FileOps(object):

    def __init__(self, db):
        self.db = db
        self.query = FileQuery(self.db)

        
    def consolidate(self, src_a, src_b, dst):
        # 1. Get all folders from both sources
        folders = query.folder_merge(src_a, src_b)

