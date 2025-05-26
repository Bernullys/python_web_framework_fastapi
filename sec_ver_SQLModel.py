from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

'''
Update the App with Multiple Models:
Now let's refactor this app a bit to increase security and versatility.
If you check the previous app, in the UI you can see that, up to now, it lets the client decide the id of the Hero to create.
We shouldn't let that happen, they could overwrite an id we already have assigned in the DB. Deciding the id should be done by the backend or the database, not by the client.
Additionally, we create a secret_name for the hero, but so far, we are returning it everywhere, that's not very secret...
We'll fix these things by adding a few extra models. Here's where SQLModel will shine.
Create Multiple Models:
In SQLModel, any model class that has table=True is a table model.
And any model class that doesn't have table=True is a data model, these ones are actually just Pydantic models (with a couple of small extra features).
With SQLModel, we can use inheritance to avoid duplicating all the fields in all the cases.

HeroBase - the base class:
Let's start with a HeroBase model that has all the fields that are shared by all the models:
name
age
'''

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


'''
Hero - the table model:
Then let's create Hero, the actual table model, with the extra fields that are not always in the other models:
id
secret_name

Because Hero inherits form HeroBase, it also has the fields declared in HeroBase, so all the fields for Hero are:
id
name
age
secret_name
'''

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

'''
HeroPublic - the public data model:
Next, we create a HeroPublic model, this is the one that will be returned to the clients of the API.
It has the same fields as HeroBase, so it won't include secret_name.
Finally, the identity of our heroes is protected!
It also re-declares id: int. By doing this, we are making a contract with the API clients, so that they can always expect the id to be there and to be an int (it will never be None).
All the fields in HeroPublic are the same as in HeroBase, with id declared as int (not None):
id
name
age
'''

class HeroPublic(HeroBase):
    id: int

'''
HeroCreate - the data model to create a hero:
Now we create a HeroCreate model, this is the one that will validate the data from the clients.
It has the same fields as HeroBase, and it also has secret_name.
Now, when the clients create a new hero, they will send the secret_name, it will be stored in the database, but those secret names won't be returned in the API to the clients.
This is how you would handle passwords. Receive them, but don't return them in the API.
You would also hash the values of the passwords before storing them, never store them in plain text.
The fields of HeroCreate are:
name
age
secret_name
'''

class HeroCreate(HeroBase):
    secret_name: str

'''
HeroCreate - the data model to create a hero:
Now we create a HeroCreate model, this is the one that will validate the data from the clients.
It has the same fields as HeroBase, and it also has secret_name.
Now, when the clients create a new hero, they will send the secret_name, it will be stored in the database, but those secret names won't be returned in the API to the clients.
This is how you would handle passwords. Receive them, but don't return them in the API.
You would also hash the values of the passwords before storing them, never store them in plain text.
The fields of HeroCreate are:
name
age
secret_name
'''

class HeroCreate(HeroBase):
    secret_name: str


'''
HeroUpdate - the data model to update a hero:
We didn't have a way to update a hero in the previous version of the app, but now with multiple models, we can do it.
The HeroUpdate data model is somewhat special, it has all the same fields that would be needed to create a new hero, but all the fields are optional (they all have a default value). This way, when you update a hero, you can send just the fields that you want to update.
Because all the fields actually change (the type now includes None and they now have a default value of None), we need to re-declare them.
We don't really need to inherit from HeroBase because we are re-declaring all the fields. I'll leave it inheriting just for consistency, but this is not necessary. It's more a matter of personal taste.
The fields of HeroUpdate are:
name
age
secret_name
'''

class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


'''
Create an Engine:
A SQLModel engine (underneath it's actually a SQLAlchemy engine) is what holds the connections to the database.
You would have one single engine object for all your code to connect to the same database.
Using check_same_thread=False allows FastAPI to use the same SQLite database in different threads. This is necessary as one single request could use more than one thread (for example in dependencies).
Don't worry, with the way the code is structured, we'll make sure we use a single SQLModel session per request later, this is actually what the check_same_thread is trying to achieve.
'''

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

'''
Create the Tables
We then add a function that uses SQLModel.metadata.create_all(engine) to create the tables for all the table models.
'''

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

'''
Create a Session Dependency:
A Session is what stores the objects in memory and keeps track of any changes needed in the data, then it uses the engine to communicate with the database.
We will create a FastAPI dependency with yield that will provide a new Session for each request. This is what ensures that we use a single session per request.
Then we create an Annotated dependency SessionDep to simplify the rest of the code that will use this dependency.
'''
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

'''
Create Database Tables on Startup:
We will create the database tables when the application starts.
Here we create the tables on an application startup event.
For production you would probably use a migration script that runs before you start your app.
Tip
SQLModel will have migration utilities wrapping Alembic, but for now, you can use Alembic directly.
'''

app = FastAPI()
#app.on_event("startup") on_even is deprecated, use life_span instead
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


'''
Create with HeroCreate and return a HeroPublic:
Now that we have multiple models, we can update the parts of the app that use them.
We receive in the request a HeroCreate data model, and from it, we create a Hero table model.
This new table model Hero will have the fields sent by the client, and will also have an id generated by the database.
Then we return the same table model Hero as is from the function. But as we declare the response_model with the HeroPublic data model, FastAPI will use HeroPublic to validate and serialize the data.
Tip
Now we use response_model=HeroPublic instead of the return type annotation -> HeroPublic because the value that we are returning is actually not a HeroPublic.
If we had declared -> HeroPublic, your editor and linter would complain (rightfully so) that you are returning a Hero instead of a HeroPublic.
By declaring it in response_model we are telling FastAPI to do its thing, without interfering with the type annotations and the help from your editor and other tools.
'''

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

'''
Read Heroes with HeroPublic:
We can do the same as before to read Heros, again, we use response_model=list[HeroPublic] to ensure that the data is validated and serialized correctly.
'''

@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

'''
Read One Hero with HeroPublic:
We can read a single hero:
'''

@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

'''
Update a Hero with HeroUpdate:
We can update a hero. For this we use an HTTP PATCH operation.
And in the code, we get a dict with all the data sent by the client, only the data sent by the client, excluding any values that would be there just for being the default values. To do it we use exclude_unset=True. This is the main trick.
Then we use hero_db.sqlmodel_update(hero_data) to update the hero_db with the data from hero_data.
'''

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

'''
Delete a Hero Again:
Deleting a hero stays pretty much the same.
We won't satisfy the desire to refactor everything in this one.
'''

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
