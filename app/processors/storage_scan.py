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
        self.db.update_record('roots', {'field': 'id', 'value': self.root_id}, {'status': 'busy'})
        
        self.update({"info": {"detail": "Scan started"}})
        sql = "SELECT * FROM `roots` WHERE `id` = %s"
        root = self.db.get_record(sql, (self.root_id,))
        self.status = "running"
        if root:
            scan = FileScan(self.db, update=self.update)
            scan.add_root(root['name'], root['path'])
            scan.process_folder('')

        self.db.update_record('roots', {'field': 'id', 'value': self.root_id}, {'status': 'ok'})
        self.done()


    def done(self):
        self.status = "done"
        self.update({"info": {"detail": "Scan completed"}})

        
    def update(self, data, immediate=False):
        current_time = int(time.perf_counter() * 1000)
        # limit rate of messsages sent
        if ((current_time - self.last_update) > 250) or immediate == True:
            self.last_update = current_time
            data["pid"] = self.pid
            data["status"] = self.status
            data["description"] = self.description
            data["action"] = "broadcast"
            try:
                asyncio.run(send(json.dumps(data), port=self.ws_port))
            except:
                sys.exit()
            

def run(description, root_id, ws_port, pid):
    ScanProcess(description, root_id, ws_port, pid).run()
