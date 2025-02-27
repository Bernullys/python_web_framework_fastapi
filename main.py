from typing import Union, Annotated, Literal
from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl



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