from fastapi import FastAPI

from fastapi_snowflake_challenge.routes.client import router as client_router

app = FastAPI()

# Include client router
app.include_router(client_router)
