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


if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    
    port = 8080
    
    if len(sys.argv) > 1:
        port = sys.argv[1]

    fh = FileHunter(port=port)
    fh.launch()
