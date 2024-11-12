import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from views import task_router

app = FastAPI()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=f"{path}/frontend"), name="static")
app.include_router(task_router, prefix="/tasks")


@app.get("/")
def read_root():
    return FileResponse(os.path.join(f"{path}/frontend", "index.html"))
