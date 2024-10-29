import os, sys, pathlib
from core.filescan import FileScan
from core.db_sqlite import Database

        
def home_dir():
    return pathlib.Path.home().resolve()


def script_dir():
    return pathlib.Path(__file__).parent.resolve()


if __name__ == '__main__':
    db = Database('test.db')

    db_file = os.path.join(script_dir(), 'test.db')
    if not os.path.exists(db_file):
        db.run_sql_file('blank.sql')

    scanner = FileScan(db)
    scanner.verbose = True
    scanner.add_root(
        'Toshiba 3Tb 3',
        '/Users/Shared/Mount/kuro/Volumes/Toshiba 3Tb 3/'
    )
