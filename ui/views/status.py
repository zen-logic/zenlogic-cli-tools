import wx

class StatusBar(wx.StatusBar):
    
    def __init__(self, parent):
        super().__init__(parent, -1)
        self.SetFieldsCount(4)
        # self.SetStatusText("", 0)
        self.SetStatusWidths([-1, -1, 100, 120])
        parent.SetStatusBar(self)


    def set_data(self, data):
        self.SetStatusText(f"Files: {data['folders']}", 2)
        self.SetStatusText(f"Folders: {data['files']}", 3)
        
