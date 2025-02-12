from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hellow": "World"}


@app.get("/items/{item_id}") # This is a path parameter item_id
def read_item(item_id: int, q: Union[str, None] = None): # This is union query. An optional query parameter q
    return {"item_id": item_id, "query": q} # These keys are hardcode here. "Ohoh" should be item_id path as int