import os, mimetypes, re
from core.handlers.base import BaseHandler
from config.settings import System

mimetypes.init()


class StaticHandler(BaseHandler):
        
    def get(self):
        file_name = self.get_physical_file_path()

        self.context.log('FILENAME: %s' % file_name)
        if os.path.exists(file_name) and os.path.isfile(file_name):
            self.create_file_buffer(file_name)
            self.done()
    

    def get_physical_file_path(self):
        path = System['static']
        for item in self.context.path_list:
            path = os.path.join(path, item)
        return path
    

    def create_file_buffer(self, file_name):
        (dummy, ext) = os.path.splitext(file_name)
        # if we can't work out the mime-type from the extension, use a default of "binary file".
        mime_type = mimetypes.types_map.get(ext, 'application/octet-stream')
        self.context.set_header('Content-type',mime_type)

        self.f = open(file_name, "rb")
        self.file_size = os.path.getsize(file_name)
        self.context.set_header('Content-length',str(self.file_size))
        self.context.buffer = self.file_buffer
        
        self.request_range = self.context.get_environment('HTTP_RANGE')
        if self.request_range:
            self.context.log('RANGE DETECTED: %s' % self.request_range)
            self.context.set_header('Accept-Ranges', 'bytes')
            self.context.status = '206 Partial Content'
            current_range = self.request_range.split('=')[-1]
            if ',' in current_range:
                self.log('multipart range not supported')
                self.not_implemented()
                return
            else:
                (range_start, range_end) = current_range.split('-')
                self.range_start = int(range_start)
                self.range_end = int(range_end)
                self.range_length = self.range_end - self.range_start + 1
                self.context.set_header('Content-Range', 'bytes %s-%s/%s' % (self.range_start, self.range_end, self.file_size))
                self.context.set_header('Content-length', self.range_length)
                self.f.seek(self.range_start, os.SEEK_SET)


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

    
handler = StaticHandler
