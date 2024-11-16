import sys
import app.main


if __name__ == '__main__':
    
    port = None
    
    if len(sys.argv) > 1:
        port = sys.argv[1]
        
    app.main.launch(use_port=port)
    
