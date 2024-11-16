import os
import time
import uuid
import mycgi as cgi
import urllib.parse
import html
import json
from tempfile import TemporaryFile
from http.cookies import SimpleCookie
from config.settings import System


class Context(object):

    def __init__(self, env=None):
        self.id = uuid.uuid4()
        self.log('Context created (%s)' % (self.id))

        self.user = None
        self.groups = ['anonymous'] # all users are 'anonymous' until authenticated
        self.token = None
        
        if env:
            self.env = env
        else:
            self.env = os.environ

        self.log(self.env)

        self.buffer = []
        self.headers = {}
        self.data = {}

        self.qs = None
        self.formdata = None
        self.readcookies = None
        self.writecookies = None

        self.method = self.get_environment('REQUEST_METHOD').lower()
        self.path = self.get_environment('PATH_INFO')

        self.path_list = list(filter(None, self.path.split('/')))
        
        # default output parameters
        self.status = '200 OK'
        self.set_header('Content-type', 'text/plain;charset=utf-8')
        self.set_header('Cache-control', 'no-cache')
        self.debug = False
        

    def __del__(self):
        self.log('Context destroyed')


    def replace_path(self, new_path):
        self.path = new_path
        self.path_list = list(filter(None, self.path.split('/')))
        

    def log(self, message, newline = True):
        if newline:
            print(str(message))
        else:
            print(str(message), end='')
                

    def error(self, e):
        import traceback
        self.status = '500 Server Error'
        self.write(str(traceback.format_exc()))
        print(str(traceback.format_exc()))
        
    
    def write(self, output):
        self.buffer.append(bytes(output, 'UTF-8'))


    def write_json(self, data):
        self.set_header('Content-type','application/json')
        # the default parameter is a function called when objects are not directly JSON serialisable
        self.buffer.append(bytes(json.dumps(data, default=str), 'UTF-8'))
        

    def set_buffer(self, buffer):
        # replace the default response buffer with a generator function/method
        self.buffer = buffer
        
        
    def get_environment(self, name):
        if name in self.env:
            return self.env[name]
        else:
            return None


    def host_name(self):
        host = self.get_environment('HTTP_HOST')
        if not host:
            host = self.get_environment('SERVER_NAME')
        else:
            host = host.split(':')[0]
        return host

    
    def get_query_string(self, name, default=None):
        if self.qs == None:
            # Returns a dictionary in which the values are lists
            self.qs = urllib.parse.parse_qs(self.get_environment('QUERY_STRING'))

        # self.log(self.qs)
            
        results = self.qs.get(name, None)

        # There can be more than one value for a variable
        # Always escape user input to avoid script injection
        if results != None:
            if len(results) > 1:
                return [html.escape(result) for result in results]
                 
            else:
                return html.escape(results[0])
        else:
            return default

        
    def debug_body(self):
        self.log('****** DEBUG ******')
        file_name = os.path.join(System['temp_path'], 'form')
        debug_file = open(file_name, 'wb')
        debug_file.write(self.body.read())
        debug_file.close()
        self.body.seek(0)
        

    def read_raw_body(self):
        self.log('read raw body')
        length = int(self.env.get('CONTENT_LENGTH', 0))
        body = self.env['wsgi.input'].read(length)
        return body

    
    def read_json_body(self):
        return json.loads(self.read_raw_body())
    
        
    def read_body(self, file_name=None):
        self.log('read formdata body')
        
        length = int(self.env.get('CONTENT_LENGTH', 0))
        if length > 0:
        
            stream = self.env['wsgi.input']
            if file_name == None:
                self.body = TemporaryFile(mode='w+b')
            else:
                self.body = open(file_name, 'wb')
            self.log('Reading form data')
            byte_count = 0
            while length > 0:
                part = stream.read(min(length, 1024*200)) # 200KB buffer size
                if not part:
                    break
                self.body.write(part)
                length -= len(part)
                byte_count += len(part)
                # self.log('read %s bytes' % (byte_count))
            self.log('Done reading')
            self.body.seek(0)
            self.env['wsgi.input'] = self.body
        else:
            self.body = None
        

    def parse_formdata(self):
        self.log('parse formdata')
        if not self.formdata:
            self.read_body()
            self.log('Parsing form data')
            if self.body != None:
                self.formdata = cgi.FieldStorage(
                    fp = self.body,
                    environ = self.env,
                    keep_blank_values = True
                )
                self.log('Done parsing')

            
    def get_form(self,name, default=None):
        if not self.formdata:
            self.parse_formdata()

        if self.formdata == None:
            return None
        elif type(self.formdata) == dict:
            if name in self.formdata:
                return(self.formdata[name])
        elif self.formdata.length > 0:
            if name in self.formdata:
                if isinstance(self.formdata[name].value, str):
                    return(self.formdata[name].value)
                else:
                    return(self.formdata[name].value.decode('utf-8'))

        return default


    def get_form_fields(self):
        if not self.formdata:
            self.parse_formdata()
        return self.formdata.keys()


    def has_form_field(self, field_name):
        if not self.formdata:
            self.parse_formdata()
        return field_name in self.formdata

    
    def set_header(self,name,value):
        self.headers[name] = value


    def get_headers(self):
        headers = []
        for header in self.headers:
            headers.append((header, str(self.headers[header])))

        if self.writecookies != None:
            for item in self.writecookies:
                cookie = tuple(self.writecookies[item].output().split(": ", 1))
                headers.append(cookie)
        
        self.log(str(headers))

        return headers

            
    def get_response(self):
        if callable(self.buffer):
            self.log('Calling response generator')
            return self.buffer()
        else:
            self.log('Sending response buffer')
            return self.buffer

        
    def get_cookie(self,name):
        if not self.readcookies:
            self.readcookies = SimpleCookie(self.get_environment('HTTP_COOKIE'))

        if name in self.readcookies:
            return(self.readcookies[name].value)
        else:
            return None


    def set_cookie(self, name, value, persist=False):
        
        if not self.writecookies:
            self.writecookies = SimpleCookie()

        self.writecookies[name] = value
        self.writecookies[name]['path'] = '/'
        # if System['domain'] != '':
        #     self.writecookies[name]['domain'] = System['domain']
            
        if persist == True:
            self.writecookies[name]['Max-Age'] = 34560000


    def remove_cookie(self, name):
        if not self.readcookies:
            self.readcookies = SimpleCookie(self.get_environment('HTTP_COOKIE'))
            
        if not self.writecookies:
            self.writecookies = SimpleCookie()

        self.writecookies[name] = 'deleted'
        self.writecookies[name]['path']='/'
        if System['domain'] != '':
            self.writecookies[name]['domain'] = System['domain']
            
        self.writecookies[name]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
            
            
    def has_data(self,key):
        key = key.upper()
        return key in self.data

    
    def get_data(self,key):
        key = key.upper()
        if key in self.data:
            return self.data[key]
        else:
            return None


    def set_data(self, name, value):
        self.data[name.upper()]=value
        

    def redirect(self, location, permanent=False):
        if permanent == True:
            self.status = '301 Moved Permanently'
        else:
            self.status = '302 Found'
        self.set_header('Location', location)
