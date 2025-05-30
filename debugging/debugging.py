import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# About __name__ == "__main__":
# The main purpose of the __name__ == "__main__" is to have some code that is executed when your file is called with: python3 debugging.py
# But is not called when another file imports it, like in: from debugging import app

# More details:
# Let's say your file is named debugging.py.
# If you run it with: python3 debugging.py
# then the internal variable __name__ in your file, created automatically by Python, will have as value the string "__main__".
# So the section uvicorn.run(app, host="0.0.0.0", port=8000) will run.
# This won't happen if you import that module (file).
# So, if you have another file importer.py with: from debugging import app
# in that case, the automatically created variable inside of debugging.py will not have the variable __name__ with a value of "__main__"
# So, the line: uvicorn.run(app, host="0.0.0.0", port=8000) won't be executed.

# Info:
# For more information, check the official Python docs.

