import wx
import wx.lib.mixins.listctrl as listmix
from ..util import *
import os, json

STATUS = {
    'online': 0,
    'busy': 1,
    'offline': 2,
    'unknown': 3
}

class StorageRoots(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, main_win, sizer, *args, **kwargs):
        self.root_items = {}
        self.main_win = main_win
        self.app = main_win.app
        self.panel_sizer = sizer
        self.selected = None
        self.timer = None
        super().__init__(style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.set_images()
        self.set_columns()

        panel_header(self.Parent, sizer, "Storage")
        sizer.Add(self, 1, flag = wx.EXPAND | wx.ALL, border=0)
        
        self.create_buttons()
        self.setup_events()

        # self.add_root({'name': 'foobar', 'status': 'online', 'idx': 0})
        # self.add_root({'name': 'foobar 2 this has quite a long title', 'status': 'busy', 'idx': 0})
        # self.add_root({'name': 'foobar 3', 'status': 'offline', 'idx': 0})
        # self.add_root({'name': 'foobar 4', 'status': 'foobar', 'idx': 0})
        # self.add_root({'name': 'foobar', 'status': 'online', 'idx': 0})
        # self.add_root({'name': 'foobar 2 this has quite a long title', 'status': 'busy', 'idx': 0})
        # self.add_root({'name': 'foobar 3', 'status': 'offline', 'idx': 0})
        # self.add_root({'name': 'foobar 4', 'status': 'foobar', 'idx': 0})


    def create_buttons(self):

        self.button_panel = wx.Panel(self.Parent)
        self.panel_sizer.Add(self.button_panel, 0, flag = wx.EXPAND | wx.ALL, border=0)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_panel.SetSizer(sizer)

        self.btn_add = wx.Button(self.button_panel, 10, "Add")
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        sizer.Add(self.btn_add, 1, flag = wx.EXPAND | wx.ALL, border=6)
        # self.btn_add.Disable()

        self.btn_rescan = wx.Button(self.button_panel, 20, "Rescan")
        self.btn_rescan.Bind(wx.EVT_BUTTON, self.on_rescan)
        sizer.Add(self.btn_rescan, 1, flag=wx.EXPAND | wx.ALL, border=6)
        self.btn_rescan.Disable()
        

    def on_add(self, evt):
        self.deselect()
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            print('You selected: %s' % dlg.GetPath())
        dlg.Destroy()


    def on_rescan(self, evt):
        print('here')
        print(evt)
        pass
    
        
    def setup_events(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect)
            

    def set_images(self):
        self.il = wx.ImageList(24, 24)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        for image in [
            'status/green.png',
            'status/amber.png',
            'status/red.png',
            'status/grey.png'
        ]:
            self.il.Add(wx.Bitmap(get_image_path(image), wx.BITMAP_TYPE_ANY))


    def set_columns(self):
        self.InsertColumn(0, "Icon")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Status", format = wx.LIST_FORMAT_RIGHT)
        self.SetColumnWidth(0, 26)
        self.setResizeColumn(2) # column id (from 1 not 0!) or 'LAST'
        
        
    def add_root(self, data):
        if not data['status'] in STATUS:
            data['status'] = 'unknown'

        idx = self.GetItemCount()
        self.Append((None,))
        self.SetItemImage(idx, STATUS.get(data['status'], 0))
        self.SetItem(idx, 1, data['name'])
        self.SetItem(idx, 2, data['status'])
        self.SetItemData(idx, data['id'])

        self.root_items[data['id']] = {
            'id': data['id'],
            'name': data['name'],
            'status': data['status'],
            'path': data['path'],
            'idx': idx
        }
        
        return idx
        

    def on_select(self, evt):
        print('select')
        self.selected = self.root_items[self.GetItemData(evt.Index)]
        if self.selected['status'] == 'online':
            self.btn_rescan.Enable()

        data = json.dumps({'dataset': self.selected})
        script = f'app.storageRoots.selectRoot({data})'
        self.main_win.webview.RunScriptAsync(script, clientData=None)
        evt.Skip()


    def on_deselect(self, evt):
        self.deselect()
        evt.Skip()
        

    def deselect(self):
        print('deselect')
        self.selected = None
        self.btn_rescan.Disable()
        for idx in range(0, self.GetItemCount(), 1):
            self.Select(idx, on=0)
            

    def set_data(self, data):
        print(data)

        if self.timer:
            self.timer.Stop()
            self.timer = None
        
        self.clear_items()
        for item in data:
            self.add_root(item)

        self.timer = wx.PyTimer(self.check_online)
        self.timer.Start(5000)
        

    def check_online(self):
        for item in self.root_items.values():
            exists = os.path.exists(item['path'])
            if exists and item['status'] == 'offline':
                item['status'] = 'online'
                self.update_root(item)
            elif not exists and item['status'] == 'online':
                item['status'] = 'offline'
                self.update_root(item)


    def update_root(self, item):
        idx = item['idx']
        self.SetItemImage(idx, STATUS.get(item['status'], 0))
        self.SetItem(idx, 1, item['name'])
        self.SetItem(idx, 2, item['status'])
            

    def clear_items(self):
        self.selected = None
        self.DeleteAllItems()
        self.root_items = {}
        
