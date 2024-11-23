import gunicorn.app.base
import gunicorn.glogging 
import gunicorn.workers.sync
import gunicorn.arbiter

from core.context import Context
from core.application import Application
import core.util
import multiprocessing as mp
import webbrowser
import subprocess
import os
import json
import signal
from core.db import Database
from config.settings import System

import core.ws


class ForkedProcess(mp.Process):
    # override default behaviour to prevent
    # AssertionError on forked processes
    def join(self, timeout=None):
        try:
            super().join(timeout=None)
        except:
            pass


class ZenServer(gunicorn.app.base.BaseApplication):
    # based on https://docs.gunicorn.org/en/stable/custom.html
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

        
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

            
    def load(self):
        return self.application


class FileHunter(object):

    def __init__(self, port=None, ws_port=None, queue=None):
        self.queue = queue
        self.host = 'localhost'
        self.port = port
        self.ws_port = ws_port
        self.server = None
        self.info = None
        self.ws = None
        db_file = os.path.join(System['data'], 'fh.db')
        self.db = Database(db_file)
        
        if not os.path.exists(db_file):
            blank = os.path.join(System['app_root'], 'core/blank.sql')
            self.db.run_sql_file(blank)
            
        self.launch()
            

    def setup(self):
        sql = "UPDATE `roots` SET `status` = 'ok'"
        self.db.execute(sql, None)
        

    def cleanup(self):
        print(f'Shutting down FileHunter server...')

        if self.ws:
            self.ws.terminate()
            self.ws.join()
            
        sql = "UPDATE `roots` SET `status` = 'ok'"
        self.db.execute(sql, None)
        sql = "DELETE FROM `processes`"
        self.db.execute(sql, None)

            
    def launch(self):

        def run(env, start_response):
            # print ('>>> process request')
            context = Context(env=env)
            application = Application(context, self)
            start_response(context.status, context.get_headers())
            return context.get_response()

        
        def ready(server):
            self.setup()
            # url = f'http://{self.host}:{self.port}'
            # webbrowser.open(url)


        def shutdown(server):
            self.cleanup()
            
            
        # workers = (mp.cpu_count() * 2) + 1
        workers = 4
        
        if not self.port:
            self.port = core.util.get_free_port()
            
        if not self.ws_port:
            self.ws_port = core.util.get_free_port()
            
        options = {
            'bind': '%s:%s' % ('0.0.0.0', self.port),
            'workers': workers,
            'when_ready': ready,
            'on_exit': shutdown,
            'errorlog': os.devnull
        }

        run_file = os.path.join(System['data'], '.run')
        with open(run_file, 'w') as f:
            data = {'pid': os.getpid(), 'host': self.host, 'port': self.port}
            f.write(json.dumps(data))
        
        # websocket server
        self.ws = self.create_process(core.ws.run, str(self.ws_port))
        # web server
        self.start_server(run, options)


    def start_server(self, run, options):
        print(f'Running FileHunter server on port {self.port}...')
        self.server = ZenServer(run, options)
        self.server.run()

        
    def create_process(self, target, *args):
        p = ForkedProcess(target=target, args=args, daemon=True)
        p.start()
        return p
        
        
    def run_background_process(self, *args):
        args = ['python', '-m'] + list(args)
        p = subprocess.Popen(args)
        
