import os
import sys
import distro

def base_dir():
    return os.getcwd()

def icon_dir():
    return os.path.join(base_dir(), 'GUI', 'pictures')

def get_os():
    system = sys.platform
    if system.startswith('linux'):
        return ('Linux',) + distro.linux_distribution()
    if system.startswith('windows'):
        return ('Windows',)
    if system.startswith('darwin'):
        return ('MacOS',)

def save_dir():
    home = os.getenv('HOME')
    data = os.path.join(home, 'deputat', 'data')
    if not os.path.exists(data):
        os.mkdir(os.path.join(home, 'deputat'))
        os.mkdir(data)
    return data