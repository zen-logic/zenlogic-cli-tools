import wx
import wx.lib.mixins.listctrl as listmix

class StorageRoots(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)

        
