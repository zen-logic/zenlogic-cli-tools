import os, sys, json, asyncio
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from websockets.asyncio.client import connect
import multiprocessing as mp
import webbrowser
import time
import wx, wx.grid
from config.settings import System
from core.server import FileHunter
import core.util


class InfoGrid(wx.grid.Grid):

    def __init__(self, parent):
        super().__init__(parent, -1)
        self.label_width = 100
        self.attr = wx.grid.GridCellAttr()
        self.EnableEditing(False)
        self.HideRowLabels()
        self.HideColLabels()
        self.SetCellHighlightPenWidth(0)
        self.SetCellHighlightROPenWidth(0)
        self.CreateGrid(0, 2)
        self.SetSelectionMode(wx.grid.Grid.GridSelectNone)
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)
        
        self.Bind(wx.EVT_SIZE, self.on_resize)

        
    def set_item(self, label, value):
        # update item if it already exists
        for idx in range(self.GetNumberRows()):
            if self.GetCellValue(idx, 0) == label:
                self.SetCellValue(idx, 0, label)
                self.SetCellValue(idx, 1, str(value))
                return
        # create new item if it doesn't
        row_id = self.GetNumberRows()
        self.AppendRows()
        self.SetRowAttr(row_id, self.attr)
        self.attr.IncRef()
        self.SetCellValue(row_id, 0, label)
        self.SetCellValue(row_id, 1, str(value))


    def remove_item(self, label):
        for idx in range(0, self.GetNumberRows()):
            if self.GetCellValue(idx, 0) == label:
                self.DeleteRows(idx, 1)
                break
        

    def on_resize(self, event):
        w, h = self.GetSize()
        self.SetColSize(0, self.label_width)
        self.SetColSize(1, w - self.label_width)

        

class StatusBar(wx.StatusBar):
    
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(1)
        self.SetStatusText("Server is not running", 0)

        

class FH(wx.MiniFrame):
    
    def __init__(self, parent):
        wx.MiniFrame.__init__(self, parent, title="File Hunter", style=wx.DEFAULT_FRAME_STYLE)
        self.server_url = f'http://localhost:8080'
        self.queue = mp.Queue()
        self.fh_server = None
        self.ws = None
        self.setup_window()
        self.attach_events()
        self.create_menu()
        self.layout()


    def layout(self):
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.info = InfoGrid(self.panel)
        self.sizer.Add(self.info, 1, wx.EXPAND|wx.ALL)
        
        self.status_bar = StatusBar(self)
        self.SetStatusBar(self.status_bar)


    def setup_window(self):
        self.SetMinSize(wx.Size(200, 100))
    
        
    def attach_events(self):
        self.Bind(wx.EVT_CLOSE, self.on_shutdown)
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_SHOW, self.on_show)


    def create_menu(self):
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        
        self.mnu_exit = menu.Append(wx.ID_EXIT,
                                    "&Quit File Hunter",
                                    helpString="Shutdown server and quit File Hunter")
        self.Bind(wx.EVT_MENU, self.on_shutdown, self.mnu_exit)

        self.mnu_start = menu.Append(wx.ID_ANY,
                                     "&Start server\tCTRL+S",
                                     helpString="Start File Hunter server")
        self.Bind(wx.EVT_MENU, self.start_server, self.mnu_start)

        menu.Append(wx.ID_SEPARATOR)
        
        self.mnu_client = menu.Append(wx.ID_ANY,
                                      "&Open Web client\tCTRL+O",
                                      helpString="Open browser window to interact with the server")
        self.Bind(wx.EVT_MENU, self.show_client, self.mnu_client)
        self.mnu_client.Enable(False)
        
        menu_bar.Append(menu, "Server")
        self.SetMenuBar(menu_bar)

        
    def on_activate(self, event):
        print('FH: activate window')

        
    def on_show(self, event):
        print('FH: show window')


    def check_server_status(self):
        run_file = os.path.join(System['data'], '.run')
        if os.path.exists(run_file):
            # load run file and check for existing server.
            with open(run_file) as f:
                data = json.load(f)
                if core.util.check_pid(data["pid"]):
                    self.server_url = f'http://{data["host"]}:{data["port"]}'
                    return(data)

        return None
                    

    def show_client(self, event):
        status = self.check_server_status()
        if status:
            webbrowser.open(self.server_url)
            return
        wx.MessageDialog(self, "Server is not available.").ShowModal()

        
    def start_server(self, event):
        if not self.fh_server:
            self.fh_server = mp.Process(target=self.start_fh_server, args=(self.queue,))
            self.fh_server.start()

            self.status = None
            while not self.status:
                self.status = self.check_server_status()
                time.sleep(.01) # wait for background process to start

            self.status_bar.SetStatusText("Server is running", 0)
            self.mnu_start.SetItemLabel("&Stop server\tCTRL+S")
            self.mnu_client.Enable(True)
            self.info.set_item('server', 'running')
            self.info.set_item('hostname', self.status["host"])
            self.info.set_item('port', self.status["port"])
            self.info.set_item('pid', self.status["pid"])
            self.info.set_item('websocket', self.status["websocket"])

            self.ws = StartCoroutine(self.ws_connect, self)
            
        else:
            self.fh_server.terminate()
            self.fh_server.join()
            self.fh_server = None
            self.status = None
            self.status_bar.SetStatusText("Server is stopped", 0)
            self.mnu_start.SetItemLabel("&Start server\tCTRL+S")
            self.mnu_client.Enable(False)
            self.info.set_item('server', 'not running')
            self.info.remove_item('hostname')
            self.info.remove_item('port')
            self.info.remove_item('pid')
            self.info.remove_item('websocket')
            
        
    def on_shutdown(self, event):

        print('FH: Shutting down...')
        self.status_bar.SetStatusText("Please wait, shutting down...", 0)

        if self.fh_server:
            # using a timer for shutdown to allow us to refresh the UI
            # because the cancel and terminate operations are blocking
            self.can_close = False
            self.timer = wx.PyTimer(self.wait_for_shutdown)
            self.timer.Start(100)
        else:
            self.Destroy()


    def wait_for_shutdown(self):
        print('waiting...')
        if not self.can_close:
            if self.ws:
                self.ws.cancel()

            if self.fh_server:
                self.fh_server.terminate()
                self.fh_server.join()
                
            self.can_close = True
                
        self.Destroy()

        
    def start_fh_server(self, queue):
        fh = FileHunter(port=None, queue=queue)


    async def ws_connect(self):
        uri = f"ws://{self.status['host']}:{self.status['websocket']}"
        print('FH:', uri)
        try:
            async with connect(uri) as websocket:
                await websocket.send('{"action": "subscribe"}')
                while True:
                    msg = await websocket.recv()
                    print('FH: recieved', msg)
                    data = json.loads(msg)
                    if 'info' in data and 'detail' in data['info']:
                        self.info.set_item('activity', data['info']['detail'])
        except Exception as e:
            print(e)
        finally:
            pass

        
# https://github.com/sirk390/wxasync
async def main_async():            
    app = WxAsyncApp()
    fh = FH(None)
    fh.Show()
    app.SetTopWindow(fh)
    await app.MainLoop()


def main():            
    app = wx.App()
    fh = FH()
    fh.Show()
    app.SetTopWindow(fh)
    app.MainLoop()
    

if __name__ == "__main__":
    import multiprocessing as mp
    mp.freeze_support()
    mp.set_start_method('fork')
    asyncio.run(main_async())
    # main()
