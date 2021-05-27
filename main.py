from fastapi import FastAPI
from database import database
import endpoints


app = FastAPI(title="CRUD for Users",
              description="Test task documentation")

app.include_router(endpoints.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
