import os
from core.handlers.base import BaseHandler
from core.template import TemplateCompiler
from config.settings import System


class MainHandler(BaseHandler):

    def get(self):
        self.context.set_header('Content-type', 'text/html')
        template = TemplateCompiler(template='pages/home',
                                    root=System['templates'],
                                    handler=self)
        

        # self.owner.run_background_process('app.test',
        #                                   'application test process',
        #                                   description='Test process')
        
        self.context.write(template.render())
        
        self.done()

        
    def test(self, *params):
        return ' '.join(list(params))
        
            
handler = MainHandler
