import os
from core.handlers.static import StaticHandler
from config.settings import System


class DefaultHandler(StaticHandler):

    def get(self):
        file_name = os.path.join(System['static'], 'index.html')
        if os.path.exists(file_name) and os.path.isfile(file_name):
            self.create_file_buffer(file_name)
            self.done()

            
handler = DefaultHandler
