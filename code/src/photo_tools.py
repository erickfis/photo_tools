"""
EMA Photo tools.

Utilities for managing photo collections.

EMA - 2023-06-17

"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from tqdm import tqdm


def get_os_creation_time(file: Path) -> datetime:
    """Get date of creation from file."""
    info = file.stat()
    date = info.st_mtime
    return datetime.fromtimestamp(date)


def archive_files(
    *, source_folder: str, destination_folder: str,
    agg_lvl: str ='day'
) -> None:
    """Scans files in folder and move each one to a subfolder.

    Backup your files before using this!

    The subfolder will be created/named after the file date of creation.
    This operation will group all files inside year-month-day
    folders.
    """
    # copy files
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
    # start scanning new folder
    folder = Path(destination_folder)
    all_files = list(folder.glob('*'))
    print(f'{len(all_files)} files to be moved.')

    if agg_lvl == 'day':
        print('Daily aggregation')
    else:
        print('Monthly aggregation')

    for file in tqdm(all_files):
        date = get_os_creation_time(file)
        if agg_lvl == 'day':
            dest = date.strftime('%Y-%m-%d')
        else:
            dest = date.strftime('%Y-%m')
        dest = file.parent / dest / file.name
        os.makedirs(dest.parent, exist_ok=True)
        file.rename(dest)


def sort_rename_files(*, source_folder: str, destination_folder: str) -> None:
    """Renames each file in folder with date of creation as prefix.

    Backup your files before using this!
    """
    # copy files
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
    # start scanning new folder
    folder = Path(destination_folder)
    all_files = list(folder.glob('*'))
    print(f'{len(all_files)} files to be renamed.')

    for file in tqdm(all_files):
        date = get_os_creation_time(file)
        prefix = date.strftime('%Y-%m-%d')
        new_fname = f'{prefix}-{file.name}'
        dest = file.parent / new_fname
        file.rename(dest)


def archive_files_by_name(
    *, source_folder: str, destination_folder: str,
    agg_lvl: str ='day'
):
    """TODO."""
    # copy files
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
    folder = pathlib.Path(destination_folder)
    all_files = list(folder.glob('*'))
    print(f'{len(all_files)} files to be moved')

    if agg_lvl == 'day':
        print('Daily aggregation')
    else:
        print('Monthly aggregation')

    for file in tqdm(all_files):
        ymd = file.name.split('_')[1]
        year = ymd[:4]
        month = ymd[4:6]
        day = ymd[6:]
        if agg_lvl != 'day':
            dest_folder = f'{year}-{month}'
        else:
            dest_folder = f'{year}-{month}-{day}'
        print(dest_folder)
        dest = file.parent / dest_folder / file.name
        os.makedirs(dest.parent, exist_ok=True)
        file.rename(dest)
