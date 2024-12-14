import wx
from ..util import *
from datetime import datetime


class Messages(wx.TextCtrl):

    def __init__(self, sizer, *args, **kwargs):
        super().__init__(*args, style = wx.TE_MULTILINE | wx.TE_READONLY, **kwargs)
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

        panel_header(self.Parent, sizer, "Message log")
        sizer.Add(self, 1, flag=wx.EXPAND|wx.ALL, border=0)
        self.write('Application started.')


    def write(self, msg):
        now = datetime.now()
        
        self.AppendText(now.strftime('%H:%M:%S '))
        self.AppendText(f'{msg}\n')
        
        
