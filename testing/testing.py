from fastapi import FastAPI
# Import TestClient:
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


# Create a TestClient by passing your FastAPI application to it:
client = TestClient(app)

# Create functions with a name that starts with test_ (this is standard pytest conventions).
# Use the TestClient object the same way as you do with httpx.
# Write simple assert statements with the standard Python expressions that you need to check (again, standard pytest).
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}