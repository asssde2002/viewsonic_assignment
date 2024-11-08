from fastapi import FastAPI
from views import task_router
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")
app.include_router(task_router, prefix="/tasks")


@app.get("/")
def read_root():
    return FileResponse(os.path.join("../frontend", "index.html"))
