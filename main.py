from typing import Union
from fastapi import FastAPI
from enum import Enum


app = FastAPI()

# The simplest FastAPI file could look like this:
@app.get("/")
def simples():
    return {"This is": "The simplest"}

# Path parameters:
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


# Predefined vaalues:

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






@app.get("/items/{item_id}") # This is a path parameter item_id
def read_item(item_id: int, q: Union[str, None] = None): # This is union query. An optional query parameter q
    return {"item_id": item_id, "query": q} # These keys are hardcode here. "Ohoh" should be item_id path as int

