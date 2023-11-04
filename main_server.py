from fastapi import FastAPI
import os
import uvicorn
from db.base import database
from db.data_base import message_types
from server.endpoints import router

from core.config import PREFIX, set_default_config



    




app = FastAPI(
    title="Employment exchange",
    docs_url=f"/docs",
    openapi_url=f"/openapi.json",
    redoc_url=None
)
app.include_router(router, tags=['main'])




@app.on_event('startup')
async def startup():
    await database.connect()
    await set_default_config(database=database)

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main_server:app', port=8080, host='0.0.0.0', reload=True)