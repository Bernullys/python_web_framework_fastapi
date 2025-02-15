from typing import Union
from fastapi import FastAPI
from enum import Enum


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
