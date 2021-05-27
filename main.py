from fastapi import FastAPI

import endpoints
from database import database


app = FastAPI(title="CRUD for Users",
              description="Test task documentation")

app.include_router(endpoints.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
