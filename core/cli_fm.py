from cli_base import BaseCLI
from fileops import FileOps

# get single file from hash to path

# combine folder to path recursively

class CLI(BaseCLI):
    
    def __init__(self, args):
        super().__init__(args)


    def setup(self):
        super().setup()
        self.ops = FileOps(self.db)

        
    # copy single file from id to path
    def copy(self):
        result = self.ops.copy_file(self.args.id, self.args.dst,
                                    root=self.args.root,
                                    mount=self.args.mount)
        if result:
            print(result)

            
    # combine items from multiple folders to path
    def merge(self):
        if self.args.recurse:
            result = self.ops.merge_folder_trees(*self.args.folders,
                                                 dst=self.args.dst,
                                                 root=self.args.root,
                                                 mount=self.args.mount)
        else:
            result = self.ops.merge_folders(*self.args.folders,
                                            dst=self.args.dst,
                                            root=self.args.root,
                                            mount=self.args.mount)
        if result:
            if isinstance(result, list):
                print('Copy errors:')
                print('  ', end='')
                print('\n  '.join(result))
            else:
                print(result)
        
