import os, sys, json, asyncio
from core.filescan import FileScan
from core.ws_client import send
from core.db import Database
from config.settings import System
import time

class ScanProcess(object):

    def __init__(self, description, root_id, ws_port, pid):
        self.status = "started"
        self.description = description
        self.pid = pid
        self.root_id = root_id
        self.ws_port = ws_port
        self.last_update = int(time.perf_counter() * 1000)
        db_file = os.path.join(System['data'], 'fh.db')
        self.db = Database(db_file)


    def run(self):
        self.update({
            "info": {"detail": "Scan started"}
        })

        time.sleep(2)
        
        sql = "SELECT * FROM `roots` WHERE `id` = %s"
        root = self.db.get_record(sql, (self.root_id,))

        self.status = "running"

        # count = 1
        # while count < 10:
        #     self.update({
        #         "info": {
        #             "detail": "ZEN LOGIC - DIAMOND - COVER LETTER.pdf",
        #             "stats": [
        #                 {"label": "Files", "value": count},
        #                 {"label": "Folders", "value": count}
        #             ]
        #         }
        #     })
        #     count += 1
        #     time.sleep(2)

        if root:
            scan = FileScan(self.db, update=self.update)
            scan.add_root(root['name'], root['path'])
            scan.process_folder('')
            
        self.done()


    def done(self):
        self.status = "done"
        self.update({"info": {"detail": "Scan completed"}})

        
    def update(self, data):
        current_time = int(time.perf_counter() * 1000)
        if (current_time - self.last_update) > 250:
            self.last_update = current_time
            data["pid"] = self.pid
            data["status"] = self.status
            data["description"] = self.description
            data["action"] = "broadcast"
            asyncio.run(send(json.dumps(data), port=self.ws_port))
            

if __name__ == "__main__":
    if len(sys.argv) > 1:
        description = sys.argv[1]
        root_id = sys.argv[2]
        ws_port = sys.argv[3]
        pid = sys.argv[4]
        ScanProcess(description, root_id, ws_port, pid).run()
