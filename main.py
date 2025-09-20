from fastapi import FastAPI
from api.routes import router
from utils.logger import setup_logger

app = FastAPI()
setup_logger()
app.include_router(router)
