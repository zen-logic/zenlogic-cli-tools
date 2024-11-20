import os
from core.handlers.base import BaseHandler
from config.settings import System
from core.filequery import FileQuery

class StatsHandler(BaseHandler):

    def get(self):
        query = FileQuery(self.owner.db)
        self.context.write_json(query.get_stats())
            
        self.done()
        # get_root(self, root_id)
        
        
handler = StatsHandler
