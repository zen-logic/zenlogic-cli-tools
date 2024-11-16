from config.settings import System
import os, shutil

class BaseHandler(object):

    def __init__(self, application):
        self.app = application
        self.context = self.app.context
        self.last_handler = False
        self.f = None
        self.path = self.context.path.split('/')

        self.context.log('>>> %s initialised' % (self.__class__.__name__))


    def done(self):
        self.last_handler = True


    def ok(self, message = None):
        self.context.status = '200 OK'
        if message == None:
            self.context.write('OK')
        else:
            self.context.write_json({
                'status': 'ok',
                'message': message
            })
            
        self.last_handler = True

        
    def not_found(self, message = None):
        self.context.status = '404 Not Found'
        if message == None:
            self.context.write('(%s) not found' % (self.context.host_name()))
        else:
            self.context.write_json({
                'status': 'error',
                'message': message
            })
        self.last_handler = True


    def invalid(self):
        self.context.status = '400 Bad Request'
        self.context.write('invalid request')
        self.last_handler = True

        
    def not_implemented(self):
        self.context.status = '501 Not Implemented'
        self.context.write('not implemented')
        self.last_handler = True

        
    def forbidden(self, message = None, login_required = True):
        self.context.status = '403 Forbidden'
        if message == None:
            self.context.write('forbidden')
        else:
            self.context.write_json({
                'status': 'forbidden',
                'message': message,
                'login_required': login_required
            })
        self.last_handler = True


    def file_buffer(self):
        """Generator to buffer file chunks"""
        byte_count = 0
        chunk_size = 1024
        while True:
            chunk = self.f.read(chunk_size)
            # time.sleep(.1)    # uncomment to simulate slow network transfer
            if not chunk:
                self.context.log('\ndone: closing file.')
                self.f.close()
                break
            yield chunk
            byte_count += len(chunk)
            
            # escape sequence is: \r (cursor to start of line), \033[2K (clear to end of line)
            # see: http://ascii-table.com/ansi-escape-sequences-vt-100.php
            self.context.log('\r\033[2Ksent %s bytes' % (byte_count), newline=False)
            # self.log('sent %s bytes' % (byte_count))


    def redirect(self, location):
        self.context.status = '302 OK'
        self.context.set_header('Location', location)
        self.last_handler = True
            
        
    def write_form_files(self):
        files = []
        self.context.log('writing form files to disk...')
        # self.context.log(str(self.context.formdata))
        
        self.context.parse_formdata()

        self.context.log('done parsing')
        
        for field in self.context.formdata.list:

            # self.context.log('field: %s' % (str(field)))
            
            if field.file and field.filename:
                path = os.path.join(System['temp_path'], self.token)
                os.makedirs(path, exist_ok=True)
                file_name = os.path.join(path, field.filename)

                # make sure file names are unique (in case multiple identically named files are uploaded)
                file_counter = 0
                while os.path.exists(file_name):
                    file_counter += 1
                    file_name = os.path.join(path, field.filename)
                    file_name = "%s_%s" % (file_name, file_counter)
                
                self.context.log('Writing: %s' % (file_name))
                f = open(file_name, 'wb')

                byte_count = 0
                chunk_size = 1024*200
                while True:
                    chunk = field.file.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    byte_count += len(chunk)
                    self.context.log('\r\033[2Kwritten %s bytes' % (byte_count), newline=False)
                self.context.log('\ndone: closing file.')
                f.close()

                files.append({
                    "file_name": field.filename,
                    "field_name": field.name,
                    "temp_path": file_name
                })

        return files


    def cleanup(self):
        self.context.log('<<< %s cleanup' % (self.__class__.__name__))
        if getattr(self, 'token', None) != None:
            path = os.path.join(System['temp_path'], self.token)
            shutil.rmtree(path, ignore_errors=True)
            if self.f != None:
                self.f.close()

            
    def run(self):
        self.context.log('running: %s (%s)' % (self.__class__.__name__, self.context.method))
        if hasattr(self, self.context.method):
            # run a method matching the request
            getattr(self, self.context.method)()
        else:
            self.context.log('no explicit %s method found' % (self.context.method))
            
        
    def __del__(self):
        self.context.log('<<< %s destroyed' % (self.__class__.__name__))


handler = BaseHandler

