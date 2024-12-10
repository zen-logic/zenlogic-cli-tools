import wx

class StatusBar(wx.StatusBar):
    
    def __init__(self, parent):
        super().__init__(parent, -1)
        self.SetFieldsCount(1)
        self.SetStatusText("This is the status", 0)
        parent.SetStatusBar(self)
