from fastapi import FastAPI

# For example, to set Swagger UI to be served at /documentation and disable ReDoc:

app = FastAPI(docs_url="/documentation", redoc_url=None)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]