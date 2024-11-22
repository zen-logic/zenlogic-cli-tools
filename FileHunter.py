import sys
from core.server import FileHunter


if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    
    port = 8080
    
    if len(sys.argv) > 1:
        port = sys.argv[1]

    fh = FileHunter(port=port)
    fh.launch()
