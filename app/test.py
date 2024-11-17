import core.db
import time, sys

count = 1
while count < 10:
    print(f'subprocess running {count} {sys.argv}')
    count += 1
    time.sleep(5)
