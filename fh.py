import sys
from core.server import FileHunter



if __name__ == '__main__':

    port = None
    
    if len(sys.argv) > 1:
        port = sys.argv[1]

    fh = FileHunter(port=port)
    fh.launch()
    
