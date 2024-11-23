from core.handlers.base import BaseHandler
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
            self.owner.create_process(process.run, description, root_id, port, pid)
            print('SCAN:',pid, root_id, port)
        self.context.write_json(response)
        self.done()

        
handler = FileScanHandler

