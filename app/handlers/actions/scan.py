import os
from core.handlers.base import BaseHandler
from config.settings import System
import core.db
import time, sys
import pathlib
import core.util
from core.filequery import FileQuery
import app.processors.storage_scan as process

class FileScanHandler(BaseHandler):

    
    def post(self):
        path = None
        response = {'status': 'OK'}
        data = self.context.read_json_body()
        if 'root' in data:
            pid = data['pid']
            description = data['description']
            root_id = str(data['root'])
            port = str(self.owner.ws_port)
            # self.owner.run_background_process('app.processors.storage_scan', description, root_id, port, pid)
            self.owner.create_process(process.run, description, root_id, port, pid)
            print('SCAN:',pid, root_id, port)
        self.context.write_json(response)
        self.done()

        
handler = FileScanHandler

