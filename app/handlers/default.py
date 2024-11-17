import os, mimetypes
from core.handlers.base import BaseHandler
from config.settings import System

mimetypes.init()


class DefaultHandler(BaseHandler):

    def get(self):
        if len(self.context.path_list) > 0:
            file_name = System['static']
            for item in self.context.path_list:
                file_name = os.path.join(file_name, item)
        else:
            file_name = os.path.join(System['static'], 'index.html')

        if os.path.exists(file_name) and os.path.isfile(file_name):
            (dummy, ext) = os.path.splitext(file_name)
            mime_type = mimetypes.types_map.get(ext, 'application/octet-stream')
            self.context.set_header('Content-type',mime_type)
            with open(file_name, "r") as f:
                self.context.write(f.read())

            self.done()

            
handler = DefaultHandler
