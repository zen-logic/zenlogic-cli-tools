import os
from core.handlers.base import BaseHandler
from config.settings import System
from core.filequery import FileQuery

class TestActionHandler(BaseHandler):

    
    def post(self):
        data = self.context.read_json_body()
        response = {'status': 'OK'}
        self.context.write_json(response)
        self.done()

        
handler = TestActionHandler
