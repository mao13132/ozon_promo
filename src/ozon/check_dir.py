import os

from pathlib import Path


def check_dirs(dir_project):
    _dir = Path(f"{dir_project}/src/browser/download")

    if not os.path.exists(_dir):
        os.mkdir(_dir)


def clear_folder(dir_project):
    import os
    _dir = Path(f"{dir_project}/src/browser/download")
    try:
        [os.remove(f'{_dir}{os.sep}{x}') for x in os.listdir(_dir)]
    except:
        return False

    return True


def one_start(dir_project):
    check_dirs(dir_project)
    clear_folder(dir_project)
