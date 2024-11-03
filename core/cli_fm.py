from cli_base import BaseCLI
from fileops import FileOps

# get single file from id to path
# get single file from hash to path
# combine folder items to path
# combine folder to path recursively

class CLI(BaseCLI):
    
    def __init__(self, args):
        super().__init__(args)


    def setup(self):
        super().setup()
        self.ops = FileOps(self.db)
        
        
    def get(self):
        result = self.ops.get_file(self.args.id, self.args.dst,
                                   root=self.args.root,
                                   mount=self.args.mount)
        print(result)
        
