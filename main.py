import aiofiles
import logging
import time
import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()
api = FastAPI()
app.mount("/api", api)

@api.get("/test")
async def test():
    return {"message": "testing the test"}

@api.post("/backup")
async def upload_backup(request: Request):
    if "get5-filename" in request.headers.keys():
        logging.info(f"get5-filename: {request.headers['get5-filename']}")
        filename = os.path.split(request.headers["get5-filename"])[-1]
    else:
        logging.info("No get5-filename header found, using default name")
        filename = f"{time.time()}.cfg"

    logging.info(f"Called POST /backup filename: {filename} and matchid: {request.headers['get5-matchid']}")

    async with aiofiles.open(os.path.join(os.getenv("BACKUP_FILE_PATH", "/usr/src/app/data"), filename), 'wb') as out_file:
        content = await request.body()
        await out_file.write(content)

    logging.info(f"Done writing file: {filename}")
    return {"filename": filename}

@api.get("/backup/{get5filename}", response_class=PlainTextResponse)
async def return_backup(request: Request):
    get5filename = request.path_params['get5filename']

    logging.info(f"Called GET /backup filename: {get5filename}")

    async with aiofiles.open(os.path.join(os.getenv("BACKUP_FILE_PATH", "/usr/src/app/data"), get5filename), 'r') as file:
        contents = await file.read()

    logging.info(f"Done returning content for file: {get5filename} content: {contents}")
    return contents
