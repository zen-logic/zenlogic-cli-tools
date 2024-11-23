import sys
from core.server import FileHunter

# imports for pyinstaller build
import core.handlers.base
import core.handlers.debug
import core.handlers.static

import app.handlers.default
import app.handlers.main
import app.handlers.notfound

import app.handlers.actions.open_folder
import app.handlers.actions.scan
import app.handlers.actions.test

import app.handlers.data.folders
import app.handlers.data.info
import app.handlers.data.path
import app.handlers.data.roots
import app.handlers.data.search
import app.handlers.data.stats


def start_server():
    port = 
    if len(sys.argv) > 1:
        port = sys.argv[1]
    fh = FileHunter(port=port)
    fh.launch()


if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    
    run_file = os.path.join(System['data'], '.run')

    if os.path.exists(run_file):
        # load run file and check for existing server.
        with open(run_file) as f:
            data = json.load(f)
            if 'pid' in data:
                if core.util.check_pid(data['pid']):
                    # there should be an existing server...
                    # we should just launch a browser pointing at
                    # the existing server and immediately exit
                    url = f'http://{data["host"]}:{data["port"]}'
                    webbrowser.open(url)
                    sys.exit()

    # no server found, launch a new one
    start_server()
