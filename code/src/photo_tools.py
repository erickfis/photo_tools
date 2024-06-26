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
    agg_lvl: str ='day', copy_first=True
) -> None:
    """Scans files in folder and move each one to a subfolder.

    Backup your files before using this!

    The subfolder will be created/named after the file date of creation.
    This operation will group all files inside year-month-day
    folders.
    """
    # copy files
    if copy_first:
        print('Copying first')
        shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
        source_folder = Path(destination_folder)
    else:
        print('not creating a copy')
        source_folder = Path(source_folder)
    # start scanning new folder
    all_files_source = list(source_folder.rglob('*.jpg'))
    print(f'{len(all_files_source)} files to be moved.')

    # if not copying first, check if files are already in dest
    if not copy_first:
        folder_dest = Path(destination_folder)
        all_files_dest = list(folder_dest.rglob('*.jpg'))

        all_files_dest_names = [item.name for item in all_files_dest]
        all_files_source_names = [item.name for item in all_files_source]

        len(all_files_dest_names), len(all_files_source_names)
        common_files = set(all_files_source_names).intersection(set(all_files_dest_names))
        print(f'there are {len(common_files)} already in destiny, skipping those')

        all_files = [item for item in all_files_source if item.name not in common_files]
    else:
        all_files = all_files_source


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
        year = date.strftime('%Y')
        complete_dest = folder_dest / year / dest / file.name
        os.makedirs(complete_dest.parent, exist_ok=True)
        if copy_first:
            file.rename(complete_dest)
        else:
            shutil.move(file, complete_dest)


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
    agg_lvl: str = 'month', copy_first=True, img_prefix=None, img_ext=None
):
    """TODO."""
    # copy files
    if copy_first:
        print('Copying first')
        shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
        folder = Path(destination_folder)
    else:
        print('not creating a copy')
        folder = Path(source_folder)

    # list files in source
    prefix = 'IMG'
    if img_prefix is not None:
        prefix = img_prefix
 
    all_files = list(folder.glob(f'{prefix}*'))

        
    print(f'{len(all_files)} files to be copyied ')

    if agg_lvl == 'day':
        print('Daily aggregation')
    else:
        print('Monthly aggregation')

    for file in tqdm(all_files):
        ymd = file.name.split('IMG')[1]
        year = ymd[:4]
        month = ymd[4:6]
        day = ymd[6:8]
        if agg_lvl == 'day':
            date = f'{year}-{month}-{day}'
        else:
            date = f'{year}-{month}'

        dest_folder = file.parent / date
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / file.name
        
        file.rename(dest_file)

