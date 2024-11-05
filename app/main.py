from fastapi import FastAPI
from app.samples.router import router as router_samples
from app.drill_hole.router import router as router_drill
from app.data_samples.router import router as router_data


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "geo hello"}


app.include_router(router_samples)
app.include_router(router_drill)
app.include_router(router_data)