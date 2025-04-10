import os
from aiofiles import open as aio_open

UPLOAD_DIR = "storage/uploads"

async def save_upload_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    async with aio_open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    return file_path
