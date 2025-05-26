from fastapi import APIRouter, Depends, HTTPException

# This code lives in the module app.routers.items, the file app/routers/items.py.
# And we need to get the dependency function from the module app.dependencies, the file app/dependencies.py.
# So we use a relative import with .. for the dependencies:

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

# But we can still add more tags that will be applied to a specific path operation, and also some extra responses specific to that path operation:  

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}

# This last path operation will have the combination of tags: ["items", "custom"].

# And it will also have both responses in the documentation, one for 404 and one for 403.

