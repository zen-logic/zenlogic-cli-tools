import core.db
import time, sys
import pathlib
import core.util


path = pathlib.Path('/Volumes').resolve()
print(path)
core.util.open_folder(path)

# count = 1
# while count < 10:
#     print(f'subprocess running {count} {sys.argv}')
#     count += 1
#     time.sleep(5)
