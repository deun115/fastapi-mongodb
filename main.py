from fastapi import FastAPI
from db.db import connect_to_mongo, close_mongo_connection
from middleware import MongoConnectionPoolLoggerMiddleware

app = FastAPI()
app.add_middleware(MongoConnectionPoolLoggerMiddleware)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()
