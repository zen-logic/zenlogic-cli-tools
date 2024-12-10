import wx, json, time
import multiprocessing as mp
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from websockets.asyncio.client import connect
from config.settings import System

from ..util import *
from ..views.info import InfoGrid
from ..views.status import StatusBar
from ..views.menu import Menu
from ..views.roots import StorageRoots
from ..views.messages import Messages

from core.server import FileHunter
import core.util



class MainWindow(wx.Frame):

    
    def __init__(self, app):
        super().__init__(None, title = System['APP_NAME'])
        self.app = app
        self._server = None
        self._ws = None
        self.server_status = None
        self.can_close = True
        self.timer = None
        self.queue = mp.Queue()
        self.layout()
        self.setup_events()
        self.refresh_status()
        self.Show(True)


    def setup_events(self):
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_ICONIZE, self.on_minimise)


    def layout(self):
        w, h = wx.DisplaySize()
        self.SetMinSize((640, 480))
        self.SetSize(w - 150, h - 200)
        
        self.Center()

        # splitters
        self.h_split = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH)
        self.h_split.SetSashGravity(0)
        self.h_split.SetMinimumPaneSize(100)
        
        self.lv_split = wx.SplitterWindow(self.h_split, -1, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH)
        self.lv_split.SetSashGravity(1)
        self.lv_split.SetMinimumPaneSize(100)

        self.rv_split = wx.SplitterWindow(self.h_split, -1, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH)
        self.rv_split.SetSashGravity(1)
        self.rv_split.SetMinimumPaneSize(100)
        
        self.h_split.SplitVertically(self.lv_split, self.rv_split, 240)

        # add panels to split zones
        pnl_items = wx.Panel(self.lv_split)
        sizer_items = wx.BoxSizer(wx.VERTICAL)
        pnl_items.SetSizer(sizer_items)

        pnl_activity = wx.Panel(self.lv_split)
        sizer_activity = wx.BoxSizer(wx.VERTICAL)
        pnl_activity.SetSizer(sizer_activity)

        self.lv_split.SplitHorizontally(pnl_items, pnl_activity, -240)
        
        pnl_webview = wx.Panel(self.rv_split)
        sizer_webview = wx.BoxSizer(wx.VERTICAL)
        pnl_webview.SetSizer(sizer_webview)
        
        pnl_log = wx.Panel(self.rv_split)
        sizer_log = wx.BoxSizer(wx.VERTICAL)
        pnl_log.SetSizer(sizer_log)

        self.rv_split.SplitHorizontally(pnl_webview, pnl_log, -200)

        # add controls to panels

        # 1. items panel
        panel_header(pnl_items, sizer_items, "Storage roots")
        
        self.items = StorageRoots(pnl_items, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER)
        self.il = wx.ImageList(24, 24)
        
        self.icn1 = self.il.Add(wx.Bitmap(get_image_path('green.png'), wx.BITMAP_TYPE_ANY))
        self.icn2 = self.il.Add(wx.Bitmap(get_image_path('amber.png'), wx.BITMAP_TYPE_ANY))
        self.icn3 = self.il.Add(wx.Bitmap(get_image_path('red.png'), wx.BITMAP_TYPE_ANY))
        self.items.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.items.InsertColumn(0, "")
        idx = self.items.InsertItem(self.items.GetItemCount(), 'foobar', 0)
        idx = self.items.InsertItem(self.items.GetItemCount(), 'foobar 2 this has quite a long title', 1)
        idx = self.items.InsertItem(self.items.GetItemCount(), 'foobar 3', 2)
        sizer_items.Add(self.items, 1, flag=wx.EXPAND|wx.ALL, border=0)
        
        # 2. info panel
        panel_header(pnl_activity, sizer_activity, "Activity")
        self.activity = InfoGrid(pnl_activity)
        # self.activity.set_item('one', 'this is value one')
        # self.activity.set_item('two', 'this is value two')
        sizer_activity.Add(self.activity, 1, flag=wx.EXPAND|wx.ALL, border=0)
        
        # 3. webview panel
        self.webview = create_webview(pnl_webview)
        sizer_webview.Add(self.webview, 1, wx.EXPAND)

        # 4. message log panel
        panel_header(pnl_log, sizer_log, "Message log")
        self.log = Messages(pnl_log)
        sizer_log.Add(self.log, 1, flag=wx.EXPAND|wx.ALL, border=0)
        self.log.write('Application started.')
        
        # other window furniture
        self.status_bar = StatusBar(self)
        self.menu = Menu(self)
        

    def on_activate(self, evt):
        print('activate...')
        evt.Skip()

        
    def on_resize(self, evt):
        print('resize...')
        evt.Skip()

        
    def on_close(self, evt):
        print('close...')
        self.shutdown()
        evt.Skip()

        
    def on_quit(self, evt):
        print('quit...')
        self.shutdown()
        evt.Skip()

        
    def on_minimise(self, evt):
        print('minimise...')
        evt.Skip()



    def refresh_status(self):
        
        if self.server_status:
            # self.status_bar.SetStatusText("Server is running", 0)
            self.menu.mnu_start.SetItemLabel("&Stop server\tCTRL+S")
            self.menu.mnu_start.SetHelp('Stop File Hunter server')

            self.activity.set_item('server', 'running')
            self.activity.set_item('hostname', self.server_status["host"])
            self.activity.set_item('port', self.server_status["port"])
            self.activity.set_item('pid', self.server_status["pid"])
            self.activity.set_item('websocket', self.server_status["websocket"])
            self.can_close = False
        else:
            # self.status_bar.SetStatusText("Server is stopped", 0)
            self.menu.mnu_start.SetItemLabel("&Start server\tCTRL+S")
            self.menu.mnu_start.SetHelp('Start File Hunter server')
            
            # self.mnu_client.Enable(False)
            self.activity.set_item('server', 'not running')
            self.activity.remove_item('hostname')
            self.activity.remove_item('port')
            self.activity.remove_item('pid')
            self.activity.remove_item('websocket')
            self.can_close = True

        

    def start_server(self, evt):
        
        def launch_server(queue):
            self.fh = FileHunter(port=None, queue=queue)

        if not self._server:
            self.log.write('Starting server, please wait...')
            self._server = mp.Process(target=launch_server, args=(self.queue,))
            self._server.start()
            self.server_status = None
            while not self.server_status:
                self.server_status = self.check_server_status()
                time.sleep(.01) # wait for background process to start

            self._ws = StartCoroutine(self.ws_connect, self)
            self.log.write('Server started.')
            self.refresh_status()
        else:
            self.stop_server()


    async def ws_connect(self):
        
        uri = f"ws://{self.server_status['host']}:{self.server_status['websocket']}"
        print('FH:', uri)
        try:
            async with connect(uri) as websocket:
                await websocket.send('{"action": "subscribe"}')
                while True:
                    msg = await websocket.recv()
                    print('FH: recieved', msg)
                    data = json.loads(msg)
                    if 'info' in data and 'detail' in data['info']:
                        self.activity.set_item('activity', data['info']['detail'])
        except Exception as e:
            print(e)
        finally:
            pass
            

    def stop_server(self):
        
        if self._server:
            self.activity.set_item('server', 'stopping...')
            self.log.write('Stopping server, please wait...')
            self.can_close = False
            self.timer = wx.PyTimer(self.wait_for_stop)
            self.timer.Start(100)


    def wait_for_stop(self):
        print('waiting...')
        if self._ws:
            self._ws.cancel()
            self._ws = None

        if self._server:
            self._server.terminate()
            self._server.join()
            self._server = None

        if self.timer:
            self.timer.Stop()
            self.timer = None
            
        self.can_close = True
        self.server_status = None
        self.log.write('Server stopped.')
        self.refresh_status()
                

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


    def shutdown(self):

        print('FH: Shutting down...')
        self.status_bar.SetStatusText("Please wait, shutting down...", 0)
        self.stop_server()

        self.Destroy()

