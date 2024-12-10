import wx

class Messages(wx.TextCtrl):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, style = wx.TE_MULTILINE, **kwargs)
        # self.log = wx.TextCtrl(pnl_log, style = wx.TE_MULTILINE)

        if wx.Platform == "__WXMAC__":
            self.OSXDisableAllSmartSubstitutions()
            self.MacCheckSpelling(False)
            self.OSXEnableAutomaticDashSubstitution(False)
            self.OSXEnableAutomaticQuoteSubstitution(False)
            
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        attr = wx.TextAttr()
        attr.SetFont(font)
        self.SetDefaultStyle(attr)


    def write(self, msg):
        self.AppendText(f'{msg}\n')
        
        
