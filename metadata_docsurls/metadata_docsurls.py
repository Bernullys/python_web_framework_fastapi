from fastapi import FastAPI

# You can set metadata for API as follows:

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Chimichanga",
    description=description,
    summary="some summary",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "name of the api",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com"
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT"
    }
)

@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]