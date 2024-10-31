import os, sys, hashlib


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
