import wx
from config.settings import System

class Menu(wx.MenuBar):

    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        menu = wx.Menu()
        
        self.mnu_exit = menu.Append(wx.ID_EXIT,
                                    "&Quit",
                                    helpString=f"Quit {System['APP_NAME']}")
        self.Bind(wx.EVT_MENU, self.app_window.on_quit, self.mnu_exit)
        self.Append(menu, 'Server')

        self.mnu_start = menu.Append(wx.ID_ANY,
                                     "&Start server\tCTRL+S",
                                     helpString="Start File Hunter server")
        self.Bind(wx.EVT_MENU, self.app_window.start_server, self.mnu_start)

        menu.Append(wx.ID_SEPARATOR)
        
        self.help_menu = wx.Menu()
        self.mnu_help = self.help_menu.Append(wx.ID_ABOUT, "&About File Hunter")
        self.Append(self.help_menu, "&Help")
        self.Bind(wx.EVT_MENU, self.app_window.show_about, self.mnu_help)

        app_window.SetMenuBar(self)
        
        
