# Zen Logic CLI tools
#### File Hunter

A command line utility and library to track, locate, match and identify duplicate files across multiple file paths, external storage (such as USB drives) or network mounts.

Scan file root and add files to database:
```shell
$ fh scan <name> <path>
```

Show available file roots:
```shell
$ fh roots
```

example output:
```
    1 Toshiba 3Tb 3        /Volumes/Toshiba 3Tb 3/
    2 G-RAID               /Volumes/G-RAID/
    3 Pegasus 1            /Volumes/Pegasus 1/
    4 EVO 970 EVO+         /Volumes/EVO 970 EVO+/
    5 Crucial 2TB          /Volumes/Crucial 2TB/
```


