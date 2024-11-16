import os, sys, pathlib


def root_dir():
    return pathlib.Path(__file__).parents[1].resolve()


System = {
    "app_root": root_dir(),
    "static": os.path.join(root_dir(), "static"),
    "handlers": [
	["^/$","app.handlers.default", "DefaultHandler"],
	["^/","core.handlers.static", "StaticHandler"],
	["^/","app.handlers.notfound", "NotFoundHandler"]
    ]
}


# from types import SimpleNamespace
# print(SimpleNamespace(System).static)
# sys.exit()
