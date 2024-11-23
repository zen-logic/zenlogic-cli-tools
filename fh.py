import os, sys, json
import webbrowser
from config.settings import System
from core.server import FileHunter
import core.util


def start_server():
    port = None
    if len(sys.argv) > 1:
        port = sys.argv[1]
    fh = FileHunter(port=port)
    fh.launch()
    

if __name__ == '__main__':
    
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
    

