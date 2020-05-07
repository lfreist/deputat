import os
import shutil

def build sep_dir():
    if os.path.exists(os.path.join(os.getcwd(), 'release', 'windows'))