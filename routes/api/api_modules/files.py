from fastapi.responses import StreamingResponse

import os

async def list_files(password):
    pw = os.getenv("GUEST_PASSWORD")

    if pw != password:
        return {"status": "false"}
    
    files = os.listdir("../../storage/api_server_files/")
    return {"list": files}

async def upload(file, password):
    pw = os.getenv("GUEST_PASSWORD")

    if pw != password:
        print(pw, password)
        return {"status": "false"}
    
    filename = file.filename
    filename = os.path.join("../../storage/api_server_files/", filename)

    if os.path.exists(filename):
        return {"message": "File already exists"}
    
    with open(filename, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

        return {"filename": file.filename, "message": "Upload successful"}
    
async def download(file_name, password):
    pw = os.getenv("GUEST_PASSWORD")

    if pw != password:
        return {"status": "false"}
    
    file_name = os.path.join("../../storage/api_server_files/", file_name)

    def file_streamer():
        with open(file_name, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(file_streamer(), media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename={file_path}"})

async def delete(file_name, password):
    pw = os.getenv("GUEST_PASSWORD")

    if pw != password:
        return {"status": "false"}
    
    file_name = os.path.join("../../storage/api_server_files/", file_name)

    if os.path.exists(file_name):
        os.remove(file_name)
        return {"message": "File deleted"}
    
    return {"message": "File not found"}