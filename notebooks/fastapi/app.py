from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


items: dict[str, Item] = {}


def update_items(item: Item) -> dict:
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    items[item.name] = item_dict
    return item_dict


def get_item(item_name: str) -> dict | None:
    if item_name in items:
        return items[item_name]
    return None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return update_items(item)


@app.get("/item/{item_name}")
async def serve_item(item_name: str):
    item = get_item(item_name)
    if not item:
        raise HTTPException(404, f"can't find {item_name}")
    return item
