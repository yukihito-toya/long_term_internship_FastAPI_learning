from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class ItemStatus(Enum):
    ON_SALE = "on_sale"
    OUT_OF_STOCK = "out_of_stock"

class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50, examples=["item1", "item2"])
    description: Optional[str] = Field(None, examples=["description1", "description2"])
    price: int = Field(gt=0, examples=[100, 200])

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, examples=["item1", "item2"])
    description: Optional[str] = Field(None, examples=["description1", "description2"])
    price: Optional[int] = Field(None, gt=0, examples=[100, 200])
    status: Optional[ItemStatus] = Field(None, examples=[ItemStatus.ON_SALE])

class Item(BaseModel):
    id: int = Field(gt=0, examples=[1, 2])
    name: str = Field(min_length=2, max_length=50, examples=["item1", "item2"])
    description: Optional[str] = Field(None, examples=["description1", "description2"])
    price: int = Field(gt=0, examples=[100, 200])
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50, examples=["user1", "user2"])
    password: str = Field(min_length=8, max_length=20, examples=["password1", "password2"])

class User(BaseModel):
    id: int = Field(gt=0, examples=[1, 2])
    username: str = Field(min_length=2, max_length=50, examples=["user1", "user2"])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    user_id: int