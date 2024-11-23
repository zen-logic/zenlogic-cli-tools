import os, sys, hashlib
import socket
from contextlib import closing
import platform, subprocess
from pathlib import Path


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


def is_windows():
    return os.name in ['nt', 'ce']


def is_macos() -> bool:
    return "darwin" in platform.system().casefold()


def open_folder(directory):
    assert isinstance(directory, Path), "ERROR: Passed a non-Path to display_folder_in_wm()!"
    assert directory.is_dir(), "ERROR! Passed a non-directory to display_folder_in_wm()!"
    
    if is_windows():
        os.startfile(os.path.normpath(directory))
    elif is_macos():
        subprocess.run(['open', str(directory)])
    else: # assume Linux or other POSIX-like
        subprocess.run(['xdg-open', str(directory)])

        
def check_pid(pid):        
    # does this PID exist as a running process?
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', int(port))) == 0    

    
