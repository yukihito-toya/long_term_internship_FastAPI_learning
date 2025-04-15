"""
Module Name: m1744254040025
Description: FastAPI router for item management
"""
from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session
from starlette import status
from modules import m1744250309517 as icluds, m1744270065338 as auth_cluds
from modules.m1744258408460 import Item, ItemCreate, ItemUpdate, TokenData
from engine_1744264596580 import get_db

DbDependency = Annotated[Session, Depends(get_db)]
TokenDependency = Annotated[TokenData, Depends(auth_cluds.get_current_user)]

rooter = APIRouter()

@rooter.get("/", response_model=list[Item], status_code=status.HTTP_200_OK)
async def get_items(db: DbDependency):
    return icluds.find_all(db)

@rooter.get("/select/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def get_item(db: DbDependency, token: TokenDependency, item_id: int = Path(gt=0)):
    item = icluds.find_by_id(db, item_id, token.user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@rooter.get("/search", response_model=list[Item], status_code=status.HTTP_200_OK)
async def search_items(db: DbDependency, name: str = Query(min_length=2, max_length=50)):
    items = icluds.find_by_name(db, name)
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return items

@rooter.post("/create", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(db: DbDependency, token: TokenDependency, item_create: ItemCreate):
    item = icluds.create_item(db, item_create, token.user_id)
    return item

@rooter.put("/update/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def update_item(db: DbDependency, token: TokenDependency, item_id: int, item_update: ItemUpdate):
    item = icluds.update_item(db, item_id, item_update, token.user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@rooter.delete("/delete/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def delete_item(db: DbDependency, token: TokenDependency, item_id: int = Path(gt=0)):
    item = icluds.delete_item(db, item_id, token.user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item