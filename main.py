from typing import Union, Annotated
from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel



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


#---------------------------------------- Request Body ----------------------------------------------------------------------------------------#

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


#--------------------------------- Query Parameters ans String Validations -------------------------------------------------#

# Additional validation: even though a query parameter is optional, whenever it is provided, its length doesn't exceed 50 characters:
@app.get("/item/")
def additional_validation(q: Annotated[str | None, Query(max_length=50)] = None):
# older version was: def additional_validation(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"items id": "Foo"}, {"item id": "Bar"}]}
    if q:
        results.update({"items id": q})
    return results

