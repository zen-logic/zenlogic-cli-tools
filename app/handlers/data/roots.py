import os
from core.handlers.base import BaseHandler
from config.settings import System
from core.filequery import FileQuery

class StorageRootsHandler(BaseHandler):

    def get(self):
        query = FileQuery(self.owner.db)
        print('='*80)
        print(self.context.path_list)
        
        if self.context.path_list[-1] == 'roots':
            self.context.write_json(query.get_roots())
        else:
            root_id = self.context.path_list[-1]
            self.context.write_json(query.get_root(root_id))
            
        self.done()
        # get_root(self, root_id)
        
        
handler = StorageRootsHandler
