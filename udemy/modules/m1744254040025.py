"""
Module Name: m1744254040025
Description: FastAPI router for item management
"""

from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session
from starlette import status
from modules import m1744250309517
from modules.m1744258408460 import Item, ItemCreate, ItemUpdate, ItemStatus
from engine_1744264596580 import get_db

DbDependency = Annotated[Session, Depends(get_db)]

rooter = APIRouter()

@rooter.get("/", response_model=list[Item], status_code=status.HTTP_200_OK)
def get_items(db: DbDependency):
    return m1744250309517.find_all(db)

@rooter.get("/select/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_item(db: DbDependency,item_id: int = Path(gt=0)):
    item = m1744250309517.find_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@rooter.get("/search", response_model=list[Item], status_code=status.HTTP_200_OK)
def search_items(db: DbDependency, name: str = Query(min_length=2, max_length=50)):
    items = m1744250309517.find_by_name(db, name)
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return items

@rooter.post("/create", response_model=ItemCreate, status_code=status.HTTP_201_CREATED)
def create_item(db: DbDependency, item_create: ItemCreate):
    item = m1744250309517.create_item(db, item_create)
    return item

@rooter.put("/update/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_item(db: DbDependency, item_id: int, item_update: ItemUpdate):
    item = m1744250309517.update_item(db, item_id, item_update)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@rooter.delete("/delete/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def delete_item(db: DbDependency, item_id: int = Path(gt=0)):
    item = m1744250309517.delete_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item