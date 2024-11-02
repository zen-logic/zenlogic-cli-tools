# Zen Logic CLI tools

## File Tools

The file tools use a local sqlite3 database to store information about files that are available to this computer.

Using the database allows quick location of files and folders as well as rapid matching (and identification) of duplicate files.

### File Hunter

A utility to track, locate and identify files and duplicates across multiple file paths, external storage (such as USB drives) or network mounts.

Scan file root and add files to database:
```shell
$ zfh scan <name> <path>
```

Show available file roots:
```shell
$ zfh roots
```

example output:
```
  1 Toshiba 3Tb 3        /Volumes/Toshiba 3Tb 3/
  2 G-RAID               /Volumes/G-RAID/
  3 Pegasus 1            /Volumes/Pegasus 1/
  4 EVO 970 EVO+         /Volumes/EVO 970 EVO+/
  5 Crucial 2TB          /Volumes/Crucial 2TB/
```


