import re, importlib, inspect
from config.settings import System
import core.db
import time


def match_handlers(uri, handlers):
    match = []
    for item in handlers:
        p = re.compile(item[0])
        if p.search(uri) != None:
            match.append(item)
    return match


class Application(object):
        
    def __init__(self, context):
        self.context = context
        self.db = None
        self.context.log('Application created')
        self.context.log('Serving: %s (%s)' % (self.context.path, self.context.method))

        self.running_handlers = []
        
        # find handlers that match this request
        matching_handlers = match_handlers(self.context.path, System['handlers'])

        modules = self.load_modules(matching_handlers)

        # time.sleep(2)
        
        for module in modules:
            if not self.run_module_handler(module):
                break

        self.cleanup()
        

    def __del__(self):
        self.context.log('Application destroyed')


    def cleanup(self):
        self.context.log('Application cleanup')

        for handler in reversed(self.running_handlers):
            handler.cleanup()
        
        if self.db != None:
            self.db.cleanup()
            self.db = None

            
    def get_database(self):
        if self.db == None:
            self.db = core.db.Database(System['db'])
        return self.db

    
    def load_modules(self, matching_handlers):
        modules = []
        for handler in matching_handlers:
            match = handler[0]
            module_path = handler[1]

            self.context.log("Matched module: '%s' => '%s'" % (match, module_path))

            # dynamically import handler
            # TODO: allow modules to be re-loaded dynamically so the server doesn't need to be restarted?
            try:
                module = importlib.import_module(module_path)
                # add "match" attribute to module for path manipulation
                setattr(module, 'match', match)
                modules.append({'module': module,
                                'handler': handler[2]})
            except Exception as e:
                module = None
                self.context.log("Error loading module: %s" % (module_path))
                self.context.log(str(e))
                self.context.error(e)
                # stop execution
                break

        if not modules:
            self.context.log("No handler match: %s" % self.context.path)
            self.context.status = '404 Not Found'
            self.context.write('handler not found');
            
        return modules

    
    
    def run_module_handler(self, module):
        self.context.log("Running handler: '%s'" % (module['module'].__name__))
        handler_object = getattr(module['module'], module['handler'], None)

        if inspect.isclass(handler_object):

            try:
                print(handler_object)
                # create a runable instance of this handler object
                handler_instance = handler_object(self)
                self.running_handlers.append(handler_instance)
                handler_instance.run()
                        
                if handler_instance.last_handler == True:
                    self.context.log('Last handler; stopping')
                    return False
                        
            except Exception as e:
                self.context.log("Handler error: %s" % (module['module'].__name__))
                self.context.log(str(e))
                self.context.error(e)
                # stop execution
                return False
        else:
            self.context.log("No callable in module %s" % (module['module'].__name__))
            self.context.status = '404 Not Found'
            self.context.write('callable not found');
            # stop execution
            return False

        return True
