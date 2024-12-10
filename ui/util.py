import os, pathlib, wx, wx.html2

def get_image_path(name):
    path = pathlib.Path(__file__).parent.resolve()
    path = os.path.join(path, 'img')
    return os.path.join(path, name)


def panel_header(parent, sizer, title):
    text = wx.StaticText(parent, -1, title)
    font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    text.SetFont(font)
    sizer.Add(text, 0, flag=wx.EXPAND|wx.ALL, border=4)
    

def create_webview(parent):
    webview = wx.html2.WebView.New(parent, backend=wx.html2.WebViewBackendDefault)
    # webview.LoadURL('https://portal.zenlogic.co.uk')
    webview.EnableAccessToDevTools(enable=True)
    webview.Hide()
    return webview
