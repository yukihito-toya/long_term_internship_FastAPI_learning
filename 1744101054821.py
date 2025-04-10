from fastapi import FastAPI, Query
from typing import Union

app = FastAPI()

fake_items_db = [{"item_name": i} for i in range(100)]

@app.get("/items/")
async def read_item(needy: str, dist: str = Query(default=None, max_length=50, pattern="^fixedquery$"), skip: int = 0, limit: Union[int, None] = None):
    if limit is None:
        limit = 10
    return needy, dist, fake_items_db[skip : skip + limit]
