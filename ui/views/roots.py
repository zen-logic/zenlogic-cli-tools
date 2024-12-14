import wx
import wx.lib.mixins.listctrl as listmix
from ..util import *

STATUS = {
    'online': 0,
    'busy': 1,
    'offline': 2,
    'unknown': 3
}

class StorageRoots(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, main_win, sizer, *args, **kwargs):
        self.main_win = main_win
        self.app = main_win.app
        self.panel_sizer = sizer
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

        btn_add = wx.Button(self.button_panel, 10, "Add")
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        sizer.Add(btn_add, 1, flag = wx.EXPAND | wx.ALL, border=6)
        btn_add.Disable()

        btn_rescan = wx.Button(self.button_panel, 20, "Rescan")
        btn_rescan.Bind(wx.EVT_BUTTON, self.on_rescan)
        sizer.Add(btn_rescan, 1, flag=wx.EXPAND | wx.ALL, border=6)
        btn_rescan.Disable()
        

    def on_add(self, evt):
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
        self.SetItemData(idx, data['idx'])

        return idx
        

    def on_select(self, evt):
        print(evt.Index)
        evt.Skip()
        

    def deselect(self):
        for idx in range(0, self.GetItemCount(), 1):
            self.Select(idx, on=0)
            
