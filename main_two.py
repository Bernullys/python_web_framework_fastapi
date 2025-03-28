from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from enum import Enum

app_two = FastAPI()

#--------------------------------------------Handling Errors------------------------------------------------#
# Raising HTTPException to handle errors:
# In this example, when the client requests an item by an ID that doesn't exist, raise an exception with a status code of 404:
items = {
    "foo": "The Foo Wrestlers"
}

@app_two.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "Item_id": item_id
    }

# Add headers to the error handler:
@app_two.get("/items/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"})
    return {
        "Item_id": item_id
    }

# Install a custom exception handler:
class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app_two.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content= {
            "message": f"Oops! {exc.name} did something extra"
        }
    )

@app_two.get("/something/{name}")
async def read_something(name: str):
    if name == "Extra":
        raise CustomException(name=name)
    return {
        "name": name
    }

# Override request validation exceptions:
@app_two.exception_handler(RequestValidationError)
async def validation_exception_handler( request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app_two.get("/override_validations/{item_id}")
async def read_item_validation(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found... Here we override the request validation exception")
    return {
        "Item_id": item_id
    }

# Override the HTTPException error handler:
@app_two.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app_two.get("/override_exceptions/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

# Use the RequestValidationError body:
@app_two.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Item(BaseModel):
    title: str
    size: int

@app_two.post("/items/")
async def create_item(item: Item):
    return item

class Item(BaseModel):
    title: str
    size: int

@app_two.post("/items/")
async def create_item(item: Item):
    return item

# Reuse FastAPI's exception handlers:
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

@app_two.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app_two.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app_two.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


#--------------------------------------------Path Operation Configuration------------------------------------------------#
# Response status code:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app_two.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item_with_status(item: Item):
    return item

# tag parameter:
@app_two.post("/items/", response_model=Item, tags=["items"])
async def create_item_with_tag(item: Item):
    return item

# Tags with Enum:
class Tags(Enum):
    items = "items"
    users = "users"

@app_two.post("/items/", response_model=Item, tags=[Tags.items])
async def create_item_with_enum_tag(item: Item):
    return item

@app_two.get("/users/", tags=[Tags.users])
async def read_users_with_enum_tag():
    return ["Rick", "Morty"]

# Summary and description:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app_two.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item

# Description from a docstring:
@app_two.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Response description:
@app_two.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Deprecate a path operation:
@app_two.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]