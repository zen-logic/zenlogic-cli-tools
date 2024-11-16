import os
from core.handlers.base import BaseHandler
from config.settings import System

class DebugHandler(BaseHandler):

    def get(self):
        self.context.write('Debug handler (GET)\n')

        self.context.write(str(self.context.env))

        self.context.write('\n')

        self.ok()
    

    def post(self):
        self.context.write('Debug handler (POST)')

        # instead of letting the context process the request body, simply
        # dump it to disk and exit

        length = int(self.context.env.get('CONTENT_LENGTH', 0))

        self.context.log('LENGTH: %s' % (length))
        
        stream = self.context.env['wsgi.input']
        file_name = os.path.join(System['temp_path'], 'request_data')
        with open(file_name, 'wb') as f:
            byte_count = 0
            while length > 0:
                part = stream.read(min(length, 1024*200)) # 200KB buffer size
                if not part:
                    break
                f.write(part)
            length -= len(part)
            byte_count += len(part)
            self.context.log('\r\033[2Kread %s bytes' % (byte_count), newline=False)
        self.context.log('\nDone reading')

        self.ok()
        
        
handler = DebugHandler
