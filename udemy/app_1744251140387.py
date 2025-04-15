"""
This is a FastAPI application that provides a RESTful API for managing items.
Udemy Learning Path: <https://www.udemy.com/course/fastapi-restapi/>
"""
import time
from fastapi import FastAPI
from modules import m1744254040025, m1744270359868
# cors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000", "https://example.com"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request, call_next):
  start_time = time.time()
  response = await call_next(request)
  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)
  return response

app.include_router(m1744254040025.rooter, prefix="/items", tags=["Items"])
app.include_router(m1744270359868.router, prefix="/auth", tags=["Auth"])
