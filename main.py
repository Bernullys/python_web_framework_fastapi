from typing import Union, Annotated, Literal, Any
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime, time, timedelta



app = FastAPI()

# The simplest FastAPI file could look like this:
@app.get("/")
def simples():
    return {"This is": "The simplest"}

#------------------------------------------- Path parameters: -----------------------------------------#
@app.get("/path_parameter/{item_id}")
def path_parameter(item_id):
    return {"Path parameter": item_id}

# Path parameters with type:
@app.get("/path_parameter_with_type/{item_id}")
def path_parameter(item_id: int):
    return {"Path parameter with type": item_id}

# Order matters:
@app.get("/order/")
def order_first():
    return {"first": "name"}

@app.get("/order/")
def order_second():
    return {"second": "second_name"}

# Or
@app.get("/order/my_name")
def order_first():
    return {"first": "name"}

@app.get("/order/{name}")
def order_second( name: str):
    return {"second": name}


# Predefined values:

class ModelName(str, Enum): # Explination in README
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


# Path convertor:

@app.get("/files/{file_path:path}")         #You could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).
async def read_file(file_path: str):        #In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home.
    return {"file_path": file_path}

# raw example of use:
@app.get("/user/{user_id}/comments")
def users_comments(user_id: int):
    return {"User_id": user_id, "Comments": {"Comment one", "Comment two"}}

#----------------------------------------------------- Query Parameters ------------------------------------------------------------------------#

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/query")
def get_with_query_parameters(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
# Example of how to use it: http://127.0.0.1:8000/query?skip=0&limit=1


# Optional parameters: Here we can leave the q query parameter empty, because is optional.
@app.get("/items/{item_id}") # This is a path parameter item_id
def read_item(item_id: int, q: Union[str, None] = None): # This q is a query parameter. An optional query parameter q using Union. New version can be done like: q: str | None = None
    if q:
        return {"item_id": item_id, "query": q} # These keys are hardcode here. "Ohoh" should be item_id path as int
    return {"item_id": item_id}

# Query parameter type conversion:
@app.get("/car/{car_id}")
def read_car(car_id: int = 0, q: str | None = None, description: bool = False):
    car = {"car_id": car_id}
    if q:
        car.update({"q": q})
    if description:
        car.update({"description": "This car has a description"})
    return car

# Multiple query parameters: with default value for a query parameter, required query parameter and optional query parameter:
@app.get("/user/{user_id}/{item_id}")
def multiple_p_q(user_id: int, item_id: int, last_name: str, name: str = "Bernardo",  nick_name: str | None = None):
    users = {"user id": user_id, "user item": item_id, "last name": last_name}
    if name:
        users.update({"name": name})
    if nick_name:
        users.update({"nick name": nick_name})
    return users


#---------------------------------------- Request Body --------------------------------------------------------------------------#

# Create a class inherited from BaseModel after importing it from pydantic
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
def create_item(item: Item):
    return item

# We can use the model inside our function:
@app.post("/item/")
def using_created_item(item: Item):
    item_dict = item.model_dump() # converts the class item to a dictionary
    if item.description is not None:
        item_dict.update({"item description": item.description})
    if item.tax is not None:
        total_price = item.price + item.tax
        item_dict.update({"Item Total Price": total_price})
    return item_dict

# Request Body + path parameters:
@app.post("/item/{item_id}")
def body_plus_path(item_id: int, item: Item):
    return {"Item id": item_id, **item.model_dump()}

# Request body + path parameters + query parameters:
@app.post("item/{item_id}")
def body_puls_path_query(item_id: int, item: Item, q: str | None = None):
    result = {"Item id": item_id, **item.model_dump()}
    if q:
        result.update({"Query parameter": q})
    return result


#--------------------------------- Query Parameters and String Validations -------------------------------------------------#

# Additional validation: even though a query parameter is optional, whenever it is provided, its length doesn't exceed 50 characters:
@app.get("/item/")
def additional_validation(q: Annotated[str | None, Query(max_length=50)] = None):
# older version was: def additional_validation(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"items id": "Foo"}, {"item id": "Bar"}]}
    if q:
        results.update({"items id": q})
    return results

# Add more validations:
@app.get("/item/")
def more_validations(q: Annotated[str | None, Query(max_length=50, min_length = 3)] =  None):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# We can add a regular expression  validation: Apart: we can find some old version using regex instead of pattern.
@app.get("/item/")
def more_validations(q: Annotated[str | None, Query(max_length=50, min_length=3, pattern="^fixedquery$")] =  None):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# We can of course use a default value different to None:
@app.get("/item/")
def other_than_none(q: Annotated[str | None, Query(max_length=50, min_length=3, pattern="^fixedquery")] = "fixedquery"):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# We can make a required value using Query only by no defining a default value:
@app.get("/item/")
def required_parameter(q: Annotated[str, Query(max_length=50, min_length=3, pattern="^fixedquery")]):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# We can required a value even if is None:
@app.get("/item/")
def required_parameter(q: Annotated[str | None, Query(max_length=50, min_length=3, pattern="^fixedquery")]):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# We can accept a list of parameters:
items = ["food", "bar"]
@app.get("/item/")
def required_parameter(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"query": q}
    return query_items
# Then, with a URL like: http://localhost:8000/items/?q=foo&q=bar

# We can accept a list of parameters with also default values:
@app.get("/item/")
def required_parameter(q: Annotated[list[str] | None, Query()] = ["food", "bar"]):
    query_items = {"query": q}
    return query_items
# Then, with a URL like: http://localhost:8000/items/ will return the default values.

# We can also use list without declaring its type.
@app.get("/item/")
def required_parameter(q: Annotated[list | None, Query()] = []):
    query_items = {"query": q}
    return query_items

# We can declare more metadata: (adding title)
@app.get("/item/")
def more_metadat(q: Annotated[str | None, Query(title="Query Title", max_length=50)]= None):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# Another example: (adding description)
@app.get("/item/")
def more_metadat(q: Annotated[str | None, 
                              Query(title="Query Title",
                                    description="This is a description",
                                     max_length=50)
                            ]= None):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# Alias parameter:
@app.get("/item/")
def alias_parameter(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item id": "Foo"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# Deprecating parameters:
@app.get("/item/")
def more_metadat(q: Annotated[str | None, 
                              Query(title="Query Title",
                                    description="This is a description",
                                     max_length=50,
                                     pattern="^fixedquery$",
                                     deprecated=True
                                     )
                            ]= None):
    results = {"items": [{"item id": "Food"}, {"item id": "Bar"}]}
    if q:
        results.update({"item id": q})
    return results

# Exclude parameters from OpenAPI (from documentation):
@app.get("/item/")
def alias_parameter(hiddien_query: Annotated[str | None, Query(include_in_schema=False)] = None):
    if hiddien_query:
        return {"hidden query": hiddien_query}
    else:
        return {"hidden query": "Not found"}


#----------------------------- Path Parameters and Numeric Validations ----------------------------------------------#
# Adding validation and metadata to a path parameter using Path: 
@app.get("/items/{item_id}")
def path_parameter_adding_metadata(
    item_id: Annotated[int , Path(title="The Id of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item id": item_id}
    if q:
        results.update({"q is": q})
    return results

# Order without using Annotated (better use it):
@app.get("/items/{item_id}")
async def required_query_and_metadata_path(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Order using Anotated:
@app.get("/items/{item_id}")
async def required_query_and_metadata_path(q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Order as you needed trick (without Annotated):
@app.get("/items/{item_id}")
async def required_query_and_metadata_path(*, item_id: int = Path(title="The ID of the item to get"), q):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Better with Annotated:
@app.get("/items/{item_id}")
async def required_query_and_metadata_path(item_id: Annotated[int, Path(title="The ID of the item to get")], q):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number Validations (ge is greater or equal than, le is less or equal than)
@app.get("/items/{item_id}")
async def number_validation(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)], q):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number Validations also work with float type but we have to use gt and lt:
@app.get("/items/{item_id}")
def float_validation(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)]
    ):
        results = {"item_id": item_id}
        if q:
            results.update({"q": q})
        if size:
            results.update({"size": size})
        return results

#-------------------------------- Query Parameter with Pydantic Model ------------------------------------------#

# Declare the query parameters in a Pydantic model, and declare the parameter as Query:
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "update_at"]
    tags: list[str] = []

@app.get("/items/")
def query_with_base_model(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

# Forbid Extra Query Parameters (using Pydantic's model configuration to forbid any extra fields)
class FilterParamsForbid(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "update_at"]
    tags: list[str] = []

@app.get("/items/")
def query_with_base_model(filter_query: Annotated[FilterParamsForbid, Query()]):
    return filter_query


#-------------------------------- Body Multiple Parameters ------------------------------------------#

# Mix Path, Query and Body parameters with Body parameters optional, by setting the default to None:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The id of the item to update", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None
    ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# More than one Body parameter
class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User
    ):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

# Singular values in Body: Extending the previous example, we can use singular values in the body (we need to import Body from fastapi):
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()]
    ):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# Multiple body params and query: we just need to add the query parameter to the function:
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
    q: str | None = None
    ):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

# Embed a single body parameter: This way should be used when we want to use a single body parameter:
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


#--------------------------------- Body - Fields ------------------------------------------#

# Declare the fields in the Pydantic model with Field:
class Item(BaseModel):
    name: str
    description: str | None = Field(None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = Field(None, description="The tax is optional")

app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


#--------------------------------- Body - Nested Models ------------------------------------------#

# This will make tags be a list, although it doesn't declare the type of the elements of the list:
class ItemBaseModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []

@app.put("/body_nested_models/{bnm_id}")
async def body_nested_models(bnm_id:int, ibm: ItemBaseModel):
    results = {"bnm id": bnm_id, "i b m": ibm}
    return results

# List fields with type parameter:
class ItemBaseModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    #we also can use set types:
    delete_duplicates_tags: set[str] = set()

@app.put("/body_nested_models_with_type_list/{bnm_id}")
async def body_nested_models_with_type_list(bnm_id:int, ibm: ItemBaseModel):
    results = {"bnm id": bnm_id, "i b m": ibm}
    return results

# Nested models:

# This is a submodel:
class Image(BaseModel):
    url: str
    # url: HttpUrl this is a special type. To use it we need to import HttpUrl from pydantic.
    name: str

class ItemsNestedModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None # here we are using a submodel as a type.

@app.put("/body_nested_models_with_nested_model/{bnm_id}")
async def body_nested_models_with_type_list(bnm_id:int, ibm: ItemsNestedModel):
    results = {"bnm id": bnm_id, "i b m": ibm}
    return results

# Nested models, special types and attributes with list of submodels:
class Image(BaseModel):
    url: HttpUrl
    name: str

class ItemsNestedModelListOfSubmodels(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

@app.put("/body_nested_models_with_nested_model_and_lists/{bnm_id}")
async def body_nested_models_with_type_list(bnm_id:int, ibm: ItemsNestedModelListOfSubmodels):
    results = {"bnm id": bnm_id, "i b m": ibm}
    return results

# Deeply nested models:
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# Bodies of pure lists:
class Image(BaseModel):
    url: HttpUrl
    name: str

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images

# Bodies of arbitrary dicts:
# In this case, you would accept any dict as long as it has int keys with float values.
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights



#--------------------------------- Declare Request Example Data ------------------------------------------#

# Declare example for Pydantic models:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
    }

@app.put("/example1/{example1_id}")
async def example1(example1_id: int, item: Item):
    results = {"example1_id": example1_id, "item": item}
    return results

# Field() additional arguments:
class Item(BaseModel):
    name: str = Field(examples = ["Bernardo"])
    description: str | None = Field(examples = ["A very nice Item"])
    price: float = Field(examples = [35.4])
    tax: float | None = Field(examples = [3.2])

@app.put("/examples_field/{item_id}")
async def examples_field(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# Body with one example:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/examples_body/{item_id}")
async def examples_body(item_id: int, item: Annotated[
    Item,
    Body(
        examples=[
            {
                "name": "Food",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            }
        ]
    )
    ]):
    results = {"item_id": item_id, "item": item}
    return results

# Body with multiple examples:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/multiple_examples_body/{item_id}")
async def multiple_examples_body(item_id: int, item: Annotated[
    Item,
    Body(
        examples=[
            {
                "name": "Food",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            },
            {
                "name": "Bar",
                "price": 3.5
            },
            {
                "name": "Baz",
                "price": 5.4,
                "tax": 1.2
            }
        ]
    )
    ]):
    results = {"item_id": item_id, "item": item}
    return results

# To show several examples in documentation:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/show_several_examples/{item_id}")
async def show_several_examples(item_id: int, item: Annotated[
    Item,
    Body(
        openapi_examples= {
            "example1": {
                "summary": "This is example 1",
                "description": "This is a complete description",
                "value": {
                    "name": "Food",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            },
            "example2": {
                "summary": "This is example 2",
                "description": "This is a complete description",
                "value": {
                    "name": "Bar",
                    "price": 3.5
                }
            },
            "example3": {
                "summary": "This is example 3",
                "description": "This is a complete description",
                "value": {
                    "name": "Baz",
                    "price": 5.4,
                    "tax": 1.2
                }
            },
        }
    )
    ]):
    results = {"item_id": item_id, "item": item}
    return results


#--------------------------------- Extra Data Types ------------------------------------------#

# Example using some extra data types:
@app.put("/items/{item_id}")
async def extra_datatypes(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item id": item_id,
        "start datetime": start_datetime,
        "end datetime": end_datetime,
        "process after": process_after,
        "repear at": repeat_at,
        "start process": start_process,
        "duration": duration
    }


#--------------------------------- Cookie Parameters ------------------------------------------#
# Cookie parameter:
@app.get("/items/")
async def cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads id": ads_id}


#--------------------------------- Header Parameters ------------------------------------------#
# Header parameter:
@app.get("/item/")
async def header(user_agent: Annotated[str | None, Header()] = None):
    return { "User-Agent": user_agent}

# Duplicate Headers, to declare a header of X-Token that can appear more than once:
@app.get("/items/")
async def duplicate_headers(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}


#--------------------------------- Cookie Parameter Models ------------------------------------------#
# Cookies with a Pydantic Model:
class Cookies(BaseModel):
    session_id: str
    fetebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def cookie_model(cookies: Annotated[Cookies, Cookie()]):
    return cookies

# Forbid Extra Cookies:
class ForbidCookies(BaseModel):
    model_config = {"extra": "forbid"}
    session_id: str
    fetebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def cookie_model_forbid(cookies: Annotated[ForbidCookies, Cookies()]):
    return cookies


#--------------------------------- Header Parameter Models ------------------------------------------#
# Header with a Pydantic Model:
class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def header_model(headers: Annotated[CommonHeaders, Header()]):
    return headers

# Forbid Extra Headers:
class ForbidHeaders(BaseModel):
    model_config = {"extra": "forbid"}
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def header_model_forbid(headers: Annotated[ForbidHeaders, Header()]):
    return headers


#--------------------------------- Response Model - Return Type ------------------------------------------#
# This is a return type annotation symbol: ->
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/")
async def create_item_using_rta(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items_usind_rta() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]

# This is a response_model parameter to ensure the data type but more flexible: (we have to import Any)
@app.post("/items/", response_model=Item)
async def create_item_using_rm(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items_using_rm() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]

# Return the same input data:
#Here we are declaring a UserIn model, it will contain a plaintext password:
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

# Don't do this in production!
@app.post("/user/")
async def create_user_return_same_input_data(user: UserIn) -> UserIn:
    return user

# Add an output model: We can instead create an input model with the plaintext password and an output model without it:
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/", response_model=UserOut)
async def create_user_return_output_data(user: UserIn) -> Any:
    return user

#Return type and Data Filtering:
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(BaseUser):
    password: str

@app.post("/user/")
async def create_user_data_filtering(user: UserIn) -> BaseUser:
    return user

# Other return type annotations:
# Return a Response directly:
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

# Annotate a Response Subclass:
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Invalid return type annotation:
@app.get("/portal")
async def get_portal_invalid(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

# Disable response_model:
@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

# Response Model encoding parameters:
# Your response model could have default values:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item_avoiding_default_values(item_id: str):
    return items[item_id]

# response_model_include and response_model_exclude:
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

# Note: The syntax {"name", "description"} creates a set with those two values.
# It is equivalent to set(["name", "description"]).

@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name_model_include(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data_model_exclude(item_id: str):
    return items[item_id]

# Using list's instead of set's:
# Changes: 
# response_model_include=["name", "description"]
# and:
# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])


#--------------------------------- Extra Models ------------------------------------------#
# Here's a general idea of how the models could look like with their password fields and the places where they are used:
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password = hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user_with_hp(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Reduce duplicarion using a BaseModel and subclasses:
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserIn):
    pass

class UserInDB(UserIn):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password = hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user_with_hp(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Union or anyOf example:
class BaseItem(BaseModel):
    description: str | None = None
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {
        "description": "All my friends drive a low rider",
        "type": "car"
    },
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item_two_different_types(item_id: str):
    return items[item_id]

# List of models:
class Item(BaseModel):
    name: str
    description: str | None = None

items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items/", response_model=list[Item])
async def read_list_of_objects_items():
    return items

# Response with arbitrary dict:
@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights_arbitrary_dict():
    return {"foo": 2.3, "bar": 3.4}

