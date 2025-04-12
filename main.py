from fastapi import FastAPI
from db.db import connect_to_mongo, close_mongo_connection
from middleware import MongoConnectionPoolLoggerMiddleware

from router.item import item_router
from router.progress import progress_router

app = FastAPI()
app.add_middleware(MongoConnectionPoolLoggerMiddleware)
app.include_router(item_router)
app.include_router(progress_router)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()
