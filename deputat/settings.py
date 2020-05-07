import os
import sys
import distro
import site
import deputat

def base_dir():
    return deputat.__path__[0]

def icon_dir():
    base = base_dir()
    return os.path.join(base, 'GUI', 'pictures')

def get_os():
    system = sys.platform
    if system.startswith('linux'):
        return ('Linux',) + distro.linux_distribution()
    if system.startswith('win'):
        return 'Windows'
    if system.startswith('darwin'):
        return 'MacOS'

def save_dir():
    home = os.getenv('HOME')
    if get_os() == 'Windows':
        from pathlib import Path
        home = str(Path.home())
    data = os.path.join(home, 'deputat_data', 'data')
    if not os.path.exists(data):
        os.mkdir(os.path.join(home, 'deputat_data'))
        os.mkdir(data)
    return data
