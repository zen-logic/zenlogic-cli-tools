import os, sys, pathlib
from core.filescan import FileScan
from core.db_sqlite import Database

        
def home_dir():
    return pathlib.Path.home().resolve()


def script_dir():
    return pathlib.Path(__file__).parent.resolve()


if __name__ == '__main__':
    db_file = os.path.join(script_dir(), 'test.db')
    db = Database(db_file)

    if not os.path.exists(db_file):
        db.run_sql_file('blank.sql')

    scanner = FileScan(db)
    scanner.verbose = True
    # scanner.add_root(
    #     'Crucial 2TB',
    #     '/Volumes/Crucial 2TB/'
    # )
    print('nothing defined')
    
