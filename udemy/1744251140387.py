"""
This is a FastAPI application that provides a RESTful API for managing items.
Udemy Learning Path: <https://www.udemy.com/course/fastapi-restapi/>
"""
from fastapi import FastAPI
from modules import m1744254040025

app = FastAPI()
app.include_router(m1744254040025.rooter, prefix="/items", tags=["Items"])
