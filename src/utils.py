import os
from pathlib import Path
import shutil
from enum import Enum


class AllowedFileTypes(str, Enum):
    markdown = '.md'


def validate_filetype(file): # file : UploadFile
    """
    Validates if the uploaded file by user is supported by application or not
    This validation takes only the extension in the file into account to check. => Need some better way
    """

    if file.filename.endswith('.md'):
        return file
    return False


# def exists(filename: str) -> bool:
#     """
#     Validates if the uploaded file already exists in the data directory
#     This validation happens based on filename => Need some better way
#     If exists, returns True
#     Otherwise, returns False
#     """
#     data_directory_absolute_path = Path(os.environ.get('DATA_DIRECTORY_ABSOLUTE_PATH'))

#     if (data_directory_absolute_path / filename).exists():
#         return True
#     return False

def create_or_update_file(file, filename: str) -> bool:
    """
    Create the file in data directory
    """
    data_directory_absolute_path = Path(os.environ.get('DATA_DIRECTORY_ABSOLUTE_PATH'))
    try:
        with open(data_directory_absolute_path / filename, '+wb') as buffer:
            shutil.copyfileobj(fsrc=file, fdst=buffer)
        return True
    except Exception as e:
        return False # Need to retry may be if possible