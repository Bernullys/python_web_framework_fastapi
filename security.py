from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

'''
Here tokenUrl="token" refers to a relative URL token that we haven't created yet. As it's a relative URL, it's equivalent to ./token.
Because we are using a relative URL, if your API was located at https://example.com/, then it would refer to https://example.com/token. But if your API was located at https://example.com/api/v1/, then it would refer to https://example.com/api/v1/token.
Using a relative URL is important to make sure your application keeps working even in an advanced use case like Behind a Proxy.
'''

'''
The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".
It could be called as:
    oauth2_scheme(some, parameters)
So, it can be used with Depends.
Now you can pass that oauth2_scheme in a dependency with Depends.
This dependency will provide a str that is assigned to the parameter token of the path operation function.
FastAPI will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).

 '''

