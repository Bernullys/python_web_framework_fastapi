# Using BackgroundTasks:
# First, import BackgroundTasks and define a parameter in your path operation function with a type declaration of BackgroundTasks:

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


# Create a task function:
# Create a function to be run as the background task.
# It is just a standard function that can receive parameters.
# It can be an async def or normal def function, FastAPI will know how to handle it correctly.
# In this case, the task function will write to a file (simulating sending an email).
# And as the write operation doesn't use async and await, we define the function with normal def:
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

# Add the background task:
# Inside of your path operation function, pass your task function to the background tasks object with the method .add_task():
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
# .add_task() receives as arguments:
# A task function to be run in the background (write_notification).
# Any sequence of arguments that should be passed to the task function in order (email).
# Any keyword arguments that should be passed to the task function (message="some notification").