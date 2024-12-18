import wx


class GeneralPage(wx.StockPreferencesPage):

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize((600, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(wx.StaticText(panel, -1, "general page"),
        #           wx.SizerFlags(1).TripleBorder())
        panel.SetSizer(sizer)
        return panel

    
    # def GetName(self):
    #     return 'File Hunter'


class AdvancedPage(wx.StockPreferencesPage):

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize((600, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(wx.StaticText(panel, -1, "advanced page"),
        #           wx.SizerFlags(1).TripleBorder())
        panel.SetSizer(sizer)
        return panel


class Preferences(wx.PreferencesEditor):
    def __init__(self):
        super().__init__()

        self.AddPage(GeneralPage(0))  # 0 is for Kind_General
        # self.AddPage(AdvancedPage(1))  # 1 is for Kind_Advanced

        
