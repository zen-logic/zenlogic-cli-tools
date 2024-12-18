

class Controller(object):


    def refresh(self):
        print('REFRESH')
        # 1. update available storage roots
        # 2. update files/folders managed

    
    def roots(self, data):
        if 'data' in data:
            self.win.roots.set_data(data['data'])
    

    def filecount(self, data):
        if 'data' in data:
            self.win.status_bar.set_data(data['data'])
