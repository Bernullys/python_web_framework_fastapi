from fastapi import FastAPI, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

def fake_decode_token(token):
    return User (
        username = token + "fakedecoded",
        email = "example@email.com",
        full_name = "Bernardo Dávila",
        desable = False
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

