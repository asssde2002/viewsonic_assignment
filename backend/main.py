from fastapi import FastAPI
from views import task_router


app = FastAPI()
app.include_router(task_router, prefix="/tasks")


@app.get("/")
def read_root():
    return {"Hello": "World"}
