import wx
import wx.html
import wx.lib.wxpTag


class AboutBox(wx.Dialog):
    text = """
<html>
    <body bgcolor="black" text="white">
        <center>
            <p><b>File Hunter 0.1</b></p>

            <p>Created by <b>Mike Kneller</b><br><br>
            Copyright &copy;2024 <b>Zen Logic</b></p>

            <p><wxp module="wx" class="Button">
                <param name="label" value="OK">
                <param name="id"    value="ID_OK">
            </wxp></p>
        </center>
    </body>
</html>
"""
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About File Hunter',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
            html.SetStandardFonts()

        html.SetPage(self.text)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth(), ir.GetHeight()) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

