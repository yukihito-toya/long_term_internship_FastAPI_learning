"""
Module Name: m1744250309517.py
Description: Item management module
"""
from sqlalchemy.orm import Session

from modules.m1744258408460 import ItemCreate, ItemUpdate
from models import Item

# class Item:
#   def __init__(
#     self,
#     id: int,
#     name: str,
#     price: int,
#     description: Optional[str],
#     status: ItemStatus,
#   ):
#     self.id = id
#     self.name = name
#     self.price = price
#     self.description = description
#     self.status = status

# items = [
#   Item(1, "item1_qwer", 100, "description1", ItemStatus.ON_SALE),
#   Item(2, "item2_asdf", 200, None, ItemStatus.OUT_OF_STOCK),
#   Item(3, "item3_erdf", 300, "description3", ItemStatus.ON_SALE),
# ]

def find_all(db: Session):
  return db.query(Item).all()

def find_by_id(db: Session, item_id: int, user_id: int) -> Item | None:
  return db.query(Item).filter(Item.id == item_id).filter(Item.user_id == user_id).first()
  # for item in items:
  #   if item.id == item_id:
  #     return item
  # return None

def find_by_name(db: Session, name: str):
  return db.query(Item).filter(Item.name.like(f"%{name}%")).all()
  # return [item for item in items if name in item.name]

def create_item(db: Session, item_create: ItemCreate, user_id: int) -> Item:
  item = Item(
    **item_create.model_dump(),
    user_id=user_id,
  )
  db.add(item)
  db.commit()
  return item

def update_item(db:Session, item_id: int, item_update: ItemUpdate, user_id: int) -> Item | None:
  # item = find_by_id(item_id)
  item = find_by_id(db, item_id, user_id)
  if item is None:
    return None
  
  if item_update.name:
    item.name = item_update.name
  if item_update.description:
    item.description = item_update.description
  if item_update.price:
    item.price = item_update.price
  if item_update.status:
    item.status = item_update.status
  db.add(item)
  db.commit()
  return item

def delete_item(db:Session, item_id: int, user_id: int) -> Item | None:
  # item = find_by_id(item_id)
  item = find_by_id(db, item_id, user_id)
  if item is None:
    return None
  # items.remove(item)
  db.delete(item)
  db.commit()
  return item