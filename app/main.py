from fastapi import FastAPI
from app.samples.router import router as router_students


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "geo hello"}


app.include_router(router_students)