import gunicorn.app.base
from core.context import Context
from core.application import Application
import core.util
import multiprocessing
import webbrowser
import subprocess
import os
from core.db import Database
from config.settings import System


class ZenServer(gunicorn.app.base.BaseApplication):
    # modified from https://docs.gunicorn.org/en/stable/custom.html
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

    def __init__(self, port=None):
        self.port = port
        self.server = None
        self.info = None
        db_file = os.path.join(System['data'], 'fh.db')
        self.db = Database(db_file)

        if not os.path.exists(db_file):
            blank = os.path.join(System['app_root'], 'core/blank.sql')
            self.db.run_sql_file(blank)
            

    def launch(self):

        def run(env, start_response):
            print ('>>> process request')
            context = Context(env=env)
            application = Application(context, self)
            start_response(context.status, context.get_headers())
            return context.get_response()

        
        def ready(server):
            url = f'http://localhost:{port}'
            webbrowser.open(url)

            
        # workers = (multiprocessing.cpu_count() * 2) + 1
        workers = 4
        
        if self.port:
            port = self.port
        else:
            port = core.util.get_free_port()
            
        options = {
            'bind': '%s:%s' % ('127.0.0.1', port),
            'workers': workers,
            'when_ready': ready
        }
        
        self.server = ZenServer(run, options)
        self.server.run()
        
        
    def run_background_process(self, *args, description=None):
        args = ['python', '-m'] + list(args)
        p = subprocess.Popen(args)
        
