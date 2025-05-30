from fastapi import FastAPI

# For example, to set it to be served at /api/v1/openapi.json:

app = FastAPI(openapi_url="/api/v1/openapi.json")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]