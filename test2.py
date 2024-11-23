import os, sys, json, wx
import webbrowser
from config.settings import System
from core.server import FileHunter
import core.util
import multiprocessing as mp
import webbrowser


class FH(wx.Frame):

    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="File Hunter")
        self.url = f'http://localhost:8080'
        self.queue = mp.Queue()
        self.fh_server = None

        self.attach_events()
        self.create_menu()

        
    def attach_events(self):
        self.Bind(wx.EVT_CLOSE, self.on_shutdown)
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_SHOW, self.on_show)


    def create_menu(self):
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        
        self.m_exit = menu.Append(wx.ID_EXIT, "&Quit File Hunter")
        self.Bind(wx.EVT_MENU, self.on_shutdown, self.m_exit)

        self.m_start = menu.Append(wx.ID_ANY, "&Start server\tCTRL+S")
        self.Bind(wx.EVT_MENU, self.start_server, self.m_start)

        self.m_client = menu.Append(wx.ID_ANY, "Show &Client\tCTRL+C")
        self.m_client.Enable(False)
        self.Bind(wx.EVT_MENU, self.show_client, self.m_client)
        
        menu_bar.Append(menu, "Server")
        self.SetMenuBar(menu_bar)
        
        
    def on_activate(self, event):
        print('activate')

        
    def on_show(self, event):
        print('show')


    def show_client(self, event):
        run_file = os.path.join(System['data'], '.run')

        if os.path.exists(run_file):
            # load run file and check for existing server.
            with open(run_file) as f:
                data = json.load(f)
                self.url = f'http://{data["host"]}:{data["port"]}'
                
        webbrowser.open(self.url)
        

    def start_server(self, event):
        if not self.fh_server:
            self.fh_server = mp.Process(target=self.start_fh_server, args=(self.queue,))
            self.fh_server.start()
            self.m_start.SetItemLabel("&Stop server\tCTRL+S")
            self.m_client.Enable(True)
        else:
            self.fh_server.terminate()
            self.fh_server.join()
            self.m_start.SetItemLabel("&Start server\tCTRL+S")
            self.m_client.Enable(False)

        
    def on_shutdown(self, event):
        print('Shutting down...')
        if self.fh_server:
            self.fh_server.terminate()
            self.fh_server.join()
        
        print('closing')
        sys.exit()

        
    def start_fh_server(self, queue):
        fh = FileHunter(port=None, queue=queue)
        fh.launch()


        
if __name__ == "__main__":
    mp.freeze_support()
    mp.set_start_method('fork')
    app = wx.App()
    fh = FH(None)
    fh.Show()
    app.MainLoop()
