import os, sys, json, asyncio
from core.filescan import FileScan
from core.ws_client import send
from core.db import Database
from config.settings import System


class ScanProcess(object):

    def __init__(self, root_id, ws_port, pid):
        self.pid = pid
        self.root_id = root_id
        self.ws_port = ws_port
        db_file = os.path.join(System['data'], 'fh.db')
        self.db = Database(db_file)


    def run(self):
        self.update('Scan process started')

        sql = "SELECT * FROM `roots` WHERE `id` = %s"
        root = self.db.get_record(sql, (self.root_id,))
        # if root:
        #     scan = FileScan(self.db)
        #     scan.add_root(root['name'], root['path'])
        #     scan.process_folder('', update=self.update)


    def update(self, message):
        data = {
            "action": "broadcast",
            "pid": self.pid,
            "message": message
        }
        asyncio.run(send(json.dumps(data), port=self.ws_port))
            

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_id = sys.argv[1]
        ws_port = sys.argv[2]
        pid = sys.argv[3]
        ScanProcess(root_id, ws_port, pid).run()
