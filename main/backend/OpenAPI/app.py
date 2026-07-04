from fastapi import FastAPI

from routes.regions_routes import router as regions_router
from routes.population_routes import router as population_router
from routes.accidents_routes import router as accidents_router
from routes.aggregates_routes import router as aggregates_router

from routes.sources_routes import router as sources_router
from routes.import_runs_routes import router as import_runs_router

app = FastAPI(
    title="German Accidents API"
)

app.include_router(regions_router)
app.include_router(accidents_router)
app.include_router(population_router)
app.include_router(aggregates_router)

app.include_router(sources_router)
app.include_router(import_runs_router)

@app.get("/")
def home():
    return {
        "message": "German Accidents API Running"
    }