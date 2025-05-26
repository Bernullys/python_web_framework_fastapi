from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

'''
The Hero class is very similar to a Pydantic model (in fact, underneath, it actually is a Pydantic model).
There are a few differences:
table=True tells SQLModel that this is a table model, it should represent a table in the SQL database, it's not just a data model (as would be any other regular Pydantic class).
Field(primary_key=True) tells SQLModel that the id is the primary key in the SQL database (you can learn more about SQL primary keys in the SQLModel docs).
By having the type as int | None, SQLModel will know that this column should be an INTEGER in the SQL database and that it should be NULLABLE.
Field(index=True) tells SQLModel that it should create a SQL index for this column, that would allow faster lookups in the database when reading data filtered by this column.
SQLModel will know that something declared as str will be a SQL column of type TEXT (or VARCHAR, depending on the database).
'''

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


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
Create a Hero:
Because each SQLModel model is also a Pydantic model, you can use it in the same type annotations that you could use Pydantic models.
For example, if you declare a parameter of type Hero, it will be read from the JSON body.
The same way, you can declare it as the function's return type, and then the shape of the data will show up in the automatic API docs UI.
Here we use the SessionDep dependency (a Session) to add the new Hero to the Session instance, commit the changes to the database, refresh the data in the hero, and then return it.
'''

@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

'''
Read Heroes:
We can read Heros from the database using a select(). We can include a limit and offset to paginate the results.
'''

@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

'''
Read One Hero:
We can read a single Hero.
'''

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

'''
Delete a Hero:
We can delete a single Hero.
'''

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}

# Then go to the /docs UI, you will see that FastAPI is using these models to document the API, and it will use them to serialize and validate the data too.