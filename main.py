from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.products_router import Products_router
from app.routers.order_router import Order_router

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Products_router)
app.include_router(Order_router)
