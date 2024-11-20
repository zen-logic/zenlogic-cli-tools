--
-- File generated with SQLiteStudio v3.4.4 on Tue Oct 29 09:11:16 2024
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: folders
CREATE TABLE IF NOT EXISTS folders (
    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
    parent   INTEGER,
    root     INTEGER,
    name     VARCHAR (250),
    fullpath VARCHAR (600),
    removed  TINYINT
                           DEFAULT '0'
);


-- Table: items
CREATE TABLE IF NOT EXISTS items (
    id       INTEGER        PRIMARY KEY AUTOINCREMENT,
    root     INTEGER,
    folder   INTEGER,
    name     VARCHAR (250),
    hash     CHARACTER (32),
    size     BIGINT,
    created  DATETIME,
    modified DATETIME,
    ext      VARCHAR (100),
    removed  TINYINT
                            DEFAULT '0'
);


-- Table: roots
CREATE TABLE IF NOT EXISTS roots (
    id   INTEGER       PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (100),
    path VARCHAR (600) 
);


-- Table: processes
CREATE TABLE IF NOT EXISTS processes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pid         INTEGER,
    name        VARCHAR(100),
    description VARCHAR(400)
);

-- Index: pid
CREATE INDEX IF NOT EXISTS pid ON processes (
    "pid"
);

-- Index: name
CREATE INDEX IF NOT EXISTS name ON processes (
    "name"
);


-- Index: ext
CREATE INDEX IF NOT EXISTS ext ON items (
    "ext"
);


-- Index: folder
CREATE INDEX IF NOT EXISTS folder ON items (
    "folder"
);


-- Index: fullpath
CREATE INDEX IF NOT EXISTS fullpath ON folders (
    "fullpath"
);

-- Index: parent
CREATE INDEX IF NOT EXISTS parent ON folders (
    "parent"
);


-- Index: hash
CREATE INDEX IF NOT EXISTS hash ON items (
    "hash"
);


-- Index: name
CREATE INDEX IF NOT EXISTS name ON items (
    "name"
);


-- Index: path
CREATE INDEX IF NOT EXISTS path ON roots (
    "path"
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
