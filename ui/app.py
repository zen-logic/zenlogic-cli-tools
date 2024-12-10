import os, sys, pathlib, asyncio
import wx

# https://github.com/sirk390/wxasync
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from config.settings import System
from .windows.main import MainWindow


class App(wx.App):

    def __init__(self):
        super().__init__()
        self.win = MainWindow(self)

        
    def run(self):
        self.MainLoop()

        
class AsyncApp(WxAsyncApp):

    def __init__(self):
        # 5ms async loop, increase duration to reduce CPU load
        super().__init__(sleep_duration=0.005)
        self.win = MainWindow(self)

        
    async def run(self):
        await self.MainLoop()


async def run():
    app = AsyncApp()
    await app.run()

        
def launch(is_async=True):
    if is_async:
        asyncio.run(run())
    else:
        app = App()
        app.run()
