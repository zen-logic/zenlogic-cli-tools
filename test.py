import os, sys, json
import webbrowser
from config.settings import System
from core.server import FileHunter
import core.util

import multiprocessing as mp



from PySide6.QtCore import QSize, Qt, QTimer, QProcess
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QAction, QIcon


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.queue = mp.Queue()
        self.server_process = None

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        
        self.setFixedSize(QSize(400, 300))
        # As well as .setFixedSize() you can also call .setMinimumSize() and .setMaximumSize()

        # Set the central widget of the Window.
        self.setCentralWidget(button)

        button_action = QAction("&Start server", self)
        button_action.triggered.connect(self.onMyToolBarButtonClick)

        
        # button_action2 = QAction("Show ", self)
        # button_action2.setStatusTip("This is your button2")
        # button_action2.triggered.connect(self.onMyToolBarButtonClick)
        # button_action2.setCheckable(True)
        

        menu = self.menuBar()

        file_menu = menu.addMenu("Server")
        file_menu.addAction(button_action)
        # file_menu.addSeparator()
        # file_menu.addAction(button_action2)

        # file_submenu = file_menu.addMenu("Submenu")
        # file_submenu.addAction(button_action2)
        self.timer = QTimer()
        self.timer.timeout.connect(self.bg_process)
        self.timer.start(500)


    def bg_process(self):
        if not self.queue.empty():
            try:
                data = self.queue.get_nowait()
            except:
                data = None
        else:
            data = None
        print(data)
        
        
    def onMyToolBarButtonClick(self, s):
        if not self.server_process:
            # self.server_process = QProcess()
            # self.server_process.start("python", ['-m', 'fh'])

            
            self.server_process = mp.Process(target=start_server, args=(self.queue,))
            # run as daemon so it terminates with the main process
            # self.server_process.daemon = True
            self.server_process.start()
        # else:
        #     self.server_process.terminate()

    def shutdown(self):
        print('Shutting down...')
        if self.server_process:
            self.server_process.terminate()
            # self.server_process.waitForFinished(-1)

            
def start_server(queue):
    fh = FileHunter(port=8080, queue=queue)
    fh.launch()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(window.shutdown)
    app.exec()
    # if window.server_process:
    #     window.server_process.terminate()
