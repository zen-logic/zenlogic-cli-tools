import os
from core.handlers.base import BaseHandler
from config.settings import System
from core.filequery import FileQuery

class InfoHandler(BaseHandler):

    def get(self):
        response = {}
        if len(self.context.path_list) == 4:
            item_id = self.context.path_list[3]
            query = FileQuery(self.owner.db)
            if self.context.path_list[2] == 'folder':
                response = query.get_folder(item_id)
                sql = "SELECT COUNT(*) AS `count` FROM `items` WHERE `folder` = %s"
                count = self.owner.db.get_record(sql, (item_id,))
                response['filecount'] = count['count']
                sql = "SELECT COUNT(*) AS `count` FROM `folders` WHERE `parent` = %s"
                count = self.owner.db.get_record(sql, (item_id,))
                response['foldercount'] = count['count']
                
            elif self.context.path_list[2] == 'file':
                response = query.get_item(item_id)
        
        self.context.write_json(response)
        self.done()
        # get_root(self, root_id)
        
        
handler = InfoHandler
