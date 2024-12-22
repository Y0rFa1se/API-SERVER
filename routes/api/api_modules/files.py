from fastapi.responses import StreamingResponse

import os

async def upload(file, password):
    pw = os.getenv("GUEST_PASSWORD")

    if pw != password:
        return {"status": "false"}
    
    filename = file.filename
    
    with open(os.path.join("../storage/api_server_files/", filename), "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

        return {"filename": file.filename, "message": "Upload successful"}
    
async def download(file_path, password):
    pw = os.getenv("GUEST_PASSWORD")

    if pw != password:
        return {"status": "false"}
    
    file_path = os.path.join("../storage/api_server_files/", file_path)

    def file_streamer():
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(file_streamer(), media_type="application/octet-stream", filename=os.path.basename(file_path), headers={"Content-Disposition": "attachment; filename={file_path}"})