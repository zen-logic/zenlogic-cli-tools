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
        
        
    def copy(self):
        result = self.ops.copy_file(self.args.id, self.args.dst,
                                   root=self.args.root,
                                   mount=self.args.mount)
        if result:
            print(result)


    def merge(self):
        result = self.ops.merge(*self.args.folders,
                                dst=self.args.dst,
                                root=self.args.root,
                                mount=self.args.mount)
        
