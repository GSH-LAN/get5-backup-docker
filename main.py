import aiofiles
from fastapi import FastAPI, Request

app = FastAPI()
api = FastAPI()
app.mount("/api", api)

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