import os
from pathlib import Path
import shutil
from enum import Enum

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from fastapi import status


load_dotenv()


class AllowedFileTypes(str, Enum):
    markdown = '.md'

def validate_file(file: UploadFile):
    """
    Validates if the uploaded file by user is supported by application or not
    This validation takes only the extension in the file into account to check. => Need some better way
    """

    if file.filename.endswith('.md'):
        return file
    return False

def exists(filename: str) -> bool:
    """
    Validates if the uploaded file already exists in the data directory
    This validation happens based on filename => Need some better way
    If exists, returns True
    Otherwise, returns False
    """
    data_directory_absolute_path = Path(os.environ.get('DATA_DIRECTORY_ABSOLUTE_PATH'))

    if (data_directory_absolute_path / filename).exists():
        return True
    return False

def create_file(file, filename: str) -> bool:
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


app = FastAPI()


@app.post("/uploadfile/", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile = Depends(validate_file)):
    if file:
        if not exists(file.filename):
            create_file(file.file, filename=file.filename) # This needs to be async. Client must not wait for upload to happen
            return {
                'upload_status': 'success'
            }
        else:
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Uploaded File Already Exists'
            )
    return HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=f'Only supports markdown file, got .{file.filename.split('.')[-1]}'
    )


@app.get('/query')
def query(q:str):
    pass


@app.delete('/reset')
def reset_vector_db():
    pass