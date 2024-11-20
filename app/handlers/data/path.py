import os
from core.handlers.base import BaseHandler
from config.settings import System
from core.filequery import FileQuery

class PathHandler(BaseHandler):

    def get(self):
        response = {}
        item_id = self.context.path_list[-1]
        query = FileQuery(self.owner.db)
        response = query.get_path(item_id)
        self.context.write_json(response)
        self.done()
        # get_root(self, root_id)
        
handler = PathHandler
