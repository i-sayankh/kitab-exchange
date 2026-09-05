from fastapi import FastAPI
from database import create_tables
from routes.user_router import user_router
from routes.book_router import book_router

app = FastAPI(
    title="Kitab Exchange",
    description="A simple book exchange platform built with FastAPI and SQLModel.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    create_tables()


app.include_router(user_router)
app.include_router(book_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Kitab Exchange API!"}
