from fastapi import FastAPI
from app.controllers import example

app = FastAPI()

app.include_router(example.router)
