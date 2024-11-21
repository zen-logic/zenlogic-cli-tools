import os
from core.handlers.base import BaseHandler
from config.settings import System
from core.filequery import FileQuery

class SearchHandler(BaseHandler):

    def post(self):
        results = []
        data = self.context.read_json_body()
        
        query = FileQuery(self.owner.db)

        case_insensitive = True

        if data['type'] == 'hash':
            results += query.find_hash(data['search'])
        
        if data['type'] == 'folders' or data['type'] == 'both':
            if data['match'] == 'exact':
                results += query.find_folder_name(data['search'])
            elif data['match'] == 'start':
                results += query.find_folder_name(data['search'], partial=True, start=True, case_insensitive=case_insensitive)
            elif data['match'] == 'contains':
                results += query.find_folder_name(data['search'], partial=True, case_insensitive=case_insensitive)

        
        if data['type'] == 'files' or data['type'] == 'both':
            if data['match'] == 'exact':
                results += query.find_file_name(data['search'])
            elif data['match'] == 'start':
                results += query.find_file_name(data['search'], partial=True, start=True, case_insensitive=case_insensitive)
            elif data['match'] == 'contains':
                results += query.find_file_name(data['search'], partial=True, case_insensitive=case_insensitive)

        # results = query.find_file_name(filename,
        #                                partial=False,
        #                                start=False,
        #                                end=False,
        #                                case_insensitive=False)

        
        self.context.write_json(results)
            
        self.done()
        # get_root(self, root_id)
        
        
handler = SearchHandler
