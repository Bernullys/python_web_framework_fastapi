# Import APIRouter

from fastapi import APIRouter

# You import it and create an "instance" the same way you would with the class FastAPI:

router = APIRouter()

# Path operations with APIRouter:

# And then you use it to declare your path operations.
# Use it the same way you would use the FastAPI class:

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

# Tip: In this example, the variable is called router, but you can name it however you want.