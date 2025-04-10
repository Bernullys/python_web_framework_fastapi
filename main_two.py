from fastapi import FastAPI, HTTPException, Request, status, Cookie, Header, Depends
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


#----------------------------------------------JASON Compatible Encoders-------------------------------------------------#
# Using jsonable_encoder function:
import datetime
from fastapi.encoders import jsonable_encoder

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

# In this example, it would convert the Pydantic model to a dict, and the datetime to a str:
@app_two.put("/items/{id}")
def update_item_using_jsonable(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data


#----------------------------------------------Body Updates-------------------------------------------------#
# Updating replacing with PUT:
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app_two.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app_two.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# Updating partial with PATCH.
# Using exclude_unset parameter to True to avoid sending values that are not set
# and also using the update parameter to update the item:
@app_two.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


#----------------------------------------------Dependencies-------------------------------------------------#
# It is just a function that can take all the same parameters that a path operation function can take:
from fastapi import Depends
from typing import Annotated

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app_two.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app_two.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# Share Annotated dependencies:
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app_two.get("/items/")
async def read_items(commons: CommonsDep):
    return commons

@app_two.get("/users/")
async def read_users(commons: CommonsDep):
    return commons

# -------- Classes as Dependencies ----------#
# We can change the dependency "dependable" common_parameters from above to the class CommonQueryParams:
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app_two.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
# Notice how we write CommonQueryParams twice in the above code.
# It is from Depends(CommonQueryParams) where FastAPI will extract the declared parameters and that is what FastAPI actually call.
# In this case Annotated[CommonQueryParams doesn't have any special meaning for FastAPI. FastAPI won't use it for data conversion, validation, etc. (as it is using the Depends(CommonQueryParams) for that).
# We could actually write:
#    commons: Annotated[Any, Depends(CommonQueryParams)]
# But declaring the type is encouraged as that way your editor will know what will be passed as the parameter commons, and then it can help you with code completion, type checks, etc.

# -------- Sub-dependencies ----------#
def query_extractor(q: str | None = None): # First dependency "dependable"
    return q

def query_or_cookie_extractor(                      # Second dependency "dependable"
    q: Annotated[str, Depends(query_extractor)],    # Declares a dependency of its own (so it's a "dependant" too)
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

@app_two.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)], # Then we can use the dependency here
):
    return {"q_or_cookie": query_or_default}
# Info: Notice that we are only declaring one dependency in the path operation function, the query_or_cookie_extractor.
# But FastAPI will know that it has to solve query_extractor first, to pass the results of that to query_or_cookie_extractor while calling it.

#----------------- Dependencies in path operation decorators -------------------#
# Add dependencies to the path operation decorator:
async def verify_token(x_token: Annotated[str | None, Header()]):
    if x_token != "fake-super-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verufy_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app_two.get("/items/", dependencies=[Depends(verify_token), Depends(verufy_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

#----------------- Global dependencies -------------------#
# Add dependencies to the FastAPI application:

async def verify_token(x_token: Annotated[str | None, Header()]):
    if x_token != "fake-super-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verufy_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

app_three = FastAPI(dependencies=[Depends(verify_token), Depends(verufy_key)])

@app_three.get("/items/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

@app_three.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

#------------------- Dependencies with yield -------------------#
# A database dependency with yield:
async def get_db():
    db = DBSession() 
    try:
        yield db    # Injected into the path operation and other dependencies.
    finally:
        db.close()  # Executed after creating the response but before sending it.

# Sub-dependencies with yield:
# dependency_c can have a dependency on dependency_b, and dependency_b on dependency_a:
async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)

async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
# In this case dependency_c, to execute its exit code, needs the value from dependency_b (here named dep_b) to still be available.
# And, in turn, dependency_b needs the value from dependency_a (here named dep_a) to be available for its exit code.

# Dependencies with yield and HTTPException:
data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}

class OwnerError(Exception):
    pass

def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")

@app_two.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item

# We should re-raise the exception in the dependency:
# Now the client will get the same HTTP 500 Internal Server Error response, but the server will have our custom InternalError in the logs.
class InternalError(Exception):
    pass

def get_username():
    try:
        yield "Rick"
    except InternalError:
        print("We don't swallow the internal error here, we raise again 😎")
        raise

@app_two.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found, there's only a plumbus here"
        )
    return item_id

# Using context managers in dependencies with yield:
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

async def get_db():
    with MySuperContextManager() as db:
        yield db