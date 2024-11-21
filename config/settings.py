import os, sys, pathlib


def home_dir():
    return pathlib.Path.home().resolve()

def script_dir():
    return pathlib.Path(__file__).parent.resolve()

def data_dir():
    path = home_dir()
    path = os.path.join(path, '.zenlogic')
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def root_dir():
    return pathlib.Path(__file__).parents[1].resolve()


System = {
    "app_root": root_dir(),
    "data": data_dir(),
    "static": os.path.join(root_dir(), "static"),
    "templates": os.path.join(root_dir(), "templates"),
    "handlers": [
	["^/$","app.handlers.main", "MainHandler"], # default page
	["(\.css|\.js|\.html)$","app.handlers.default", "DefaultHandler"], # text type files
	["^/data/roots","app.handlers.data.roots", "StorageRootsHandler"],
	["^/data/folders","app.handlers.data.folders", "FoldersHandler"],
	["^/data/search","app.handlers.data.search", "SearchHandler"],
	["^/data/stats","app.handlers.data.stats", "StatsHandler"],
	["^/data/info","app.handlers.data.info", "InfoHandler"],
	["^/data/path","app.handlers.data.path", "PathHandler"],
	["^/actions/test","app.handlers.actions.test", "TestActionHandler"],
	["^/actions/folder","app.handlers.actions.open_folder", "OpenFolderHandler"],
	["^/actions/scan","app.handlers.actions.scan", "FileScanHandler"],
	["^/","core.handlers.static", "StaticHandler"],
	["^/","app.handlers.notfound", "NotFoundHandler"]
    ]
}

