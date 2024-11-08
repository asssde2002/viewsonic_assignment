from fastapi import FastAPI
from views import task_router
from fastapi.responses import FileResponse

app = FastAPI()
app.include_router(task_router, prefix="/tasks")


@app.get("/")
def read_root():
    return FileResponse("../frontend/index.html")
