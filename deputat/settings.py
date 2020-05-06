import os
import sys
import distro
import site

def base_dir():
    return os.getcwd()

def icon_dir():
    if 'deputat' in os.listdir(site.USER_SITE):
        return os.path.join(site.USER_SITE, 'deputat', 'GUI', 'pictures')
    return os.path.join(base_dir(), 'GUI', 'pictures')

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
    print(get_os())
    if get_os() == 'Windows':
        from pathlib import Path
        home = str(Path.home())
    data = os.path.join(home, 'deputat_data', 'data')
    if not os.path.exists(data):
        os.mkdir(os.path.join(home, 'deputat_data'))
        os.mkdir(data)
    return data
