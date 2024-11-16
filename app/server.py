import gunicorn.app.base


class ZenServer(gunicorn.app.base.BaseApplication):
    # copied from https://docs.gunicorn.org/en/stable/custom.html
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

        
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

            
    def load(self):
        return self.application


    def when_ready(self):
        print('READY!!!')
