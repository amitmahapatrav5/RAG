from fastapi import UploadFile
from fastapi import APIRouter, Depends, status
from fastapi import HTTPException

from utils import validate_filetype, create_or_update_file


router = APIRouter()

@router.post("/uploadfile/", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile = Depends(validate_filetype)):
    if file:        
        create_or_update_file(file.file, filename=file.filename) # This needs to be async. Client must not wait for upload to happen
        return {
            'upload_status': 'success'
        }
        
    return HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=f'Only supports markdown file, got .{file.filename.split('.')[-1]}'
    )