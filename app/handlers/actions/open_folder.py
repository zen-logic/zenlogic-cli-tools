import os
from core.handlers.base import BaseHandler
from config.settings import System
import core.db
import time, sys
import pathlib
import core.util
from core.filequery import FileQuery


class OpenFolderHandler(BaseHandler):

    
    def post(self):
        path = None
        response = {'status': 'OK'}
        data = self.context.read_json_body()
        query = FileQuery(self.owner.db)

        if 'folder' in data:
            folder = query.get_folder(data['folder'])
            path = os.path.join(folder['rootpath'], folder['fullpath'])
            path = pathlib.Path(path).resolve()

        elif 'file' in data:
            item = query.get_item(data['file'])
            folder = query.get_folder(item['folder'])
            path = os.path.join(folder['rootpath'], folder['fullpath'])
            path = pathlib.Path(path).resolve()

        if path:
            try:
                core.util.open_folder(path)
            except:
                response = {'status': 'Error', 'message': 'Folder not found'}
                
        self.context.write_json(response)
        self.done()

        
handler = OpenFolderHandler

