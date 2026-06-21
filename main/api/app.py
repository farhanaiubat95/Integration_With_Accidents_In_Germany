from fastapi import FastAPI

from routes.regions_routes import router as regions_router
from routes.population_routes import router as population_router
from routes.accidents_routes import router as accidents_router

app = FastAPI(
    title="German Accidents API"
)

app.include_router(regions_router)
app.include_router(accidents_router)
app.include_router(population_router)


@app.get("/")
def home():
    return {
        "message": "German Accidents API Running"
    }