from core.filescan import FileScan
import core.db


if __name__ == '__main__':
    import config
    db = core.db.Database(config.db)
    scanner = FileScan(db)
    scanner.verbose = True
    scanner.add_root(
        'Toshiba 3Tb 3',
        '/Users/Shared/Mount/kuro/Volumes/Toshiba 3Tb 3/'
    )

    
