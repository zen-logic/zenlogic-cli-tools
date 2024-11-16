import os, sys, hashlib
import socket
from contextlib import closing


def bytes_to_readable(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_file_hash(file_path):
    try:
        with open(file_path, 'rb', buffering=0) as f:
            digest = hashlib.file_digest(f, 'md5').hexdigest()
    except OSError as e:
        digest = None
        
    return digest


def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
