from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header

# Now we import the other submodules that have APIRouters:

from .internal import admin
from .routers import items, users

# You import and create a FastAPI class as normally.

# And we can even declare global dependencies that will be combined with the dependencies for each APIRouter:

app = FastAPI(dependencies=[Depends(get_query_token)])

# Now, let's include the routers from the submodules users and items:

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}