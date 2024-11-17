import os, sys
from string import Formatter


class TemplateDict(dict):

    
    def __new__(cls, data, owner=None):
        return super().__new__(cls, data)

    
    def __init__(self, data, owner=None):
        self.owner = owner
        self.add_actions()
        dict.__init__(self, data)
        
    
    def __missing__(self, key):

        s = key.split(' ')
        if len(s) > 1:
            action = s[0]
            params = s[1:]
        else:
            action = s[0]
            params = []
            
        if action in self.actions:
            return self.actions.get(action, self.invalid)(*params)
        else:
            # return the original key unchanged
            return "{%s}" % (key)


    def add_actions(self):
        self.actions = {
            'insert': self.insert, # insert another template
            'call': self.call, # call handler method
        }
        

    def invalid(self, key):
        return 'invalid processing instruction: %s' % (key)

    
    def not_implemented(self, key):
        return '%s not implemented' % (key[0])

    
    def insert(self, template):
        compiler = TemplateCompiler(
            root = self.owner.template_root,
            template = template,
            data = self.owner.data,
            handler = self.owner.handler
        )
        return compiler.render()


    def call(self, *params):
        method = params[0]
        params = params[1:]
        if self.owner.handler:
            handler = getattr(self.owner.handler, method, None)
            if handler:
                handler_method = getattr(self.owner.handler, method, None)
                if handler_method:
                    return handler_method(*params)

        return ''
        

class TemplateCompiler():

    
    def __init__(self, data={}, template=None, root='', handler=None):
        self.template = None
        self.data = data
        self.handler = handler
        if template:
            self.load_template(root, template)
    

    def load_template(self, template_root, template_name):
        self.template_root = template_root
        self.template_name = template_name
        filename = '%s.template' % (os.path.join(template_root, template_name))
        if os.path.exists(filename):
            with open(filename, encoding = 'utf-8') as f:
                self.template = f.read()


    def get_template_keys(self):
        return [i[1] for i in Formatter().parse(self.template) if i[1] is not None]


    def set_data(self, key, value):
        if key in self.data:
            self.data[key] += value
        else:
            self.data[key] = value
    
    
    def render(self):
        if self.template != None:
            td = TemplateDict(self.data, owner=self)
            output = self.template.format_map(td)
            return output
        else:
            return f'Missing template: {self.template_name}'
