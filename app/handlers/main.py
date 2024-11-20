import os
from core.handlers.base import BaseHandler
from core.template import TemplateCompiler
from config.settings import System


class MainHandler(BaseHandler):

    def get(self):
        self.context.set_header('Content-type', 'text/html')
        template = TemplateCompiler(template='pages/main',
                                    root=System['templates'],
                                    handler=self)

        self.context.write(template.render())
        self.done()


    def get_port(self, *params):
        return self.owner.ws_port
        
            
handler = MainHandler
