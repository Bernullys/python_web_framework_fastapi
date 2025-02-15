# python_web_framework_fastapi
Youtube course from Bitfumes

FastAPI Intro:
    Automatic docs:
        Swagger UI
        ReDoc
    Just Modern Python
        Python 3.6 with type using Pydantic
    Based on open standards
        JSON Schema
        Open API
    Vscode Editor support and Pycharm too
    Security and authentication:
        HTTP Basic
        OAuth2 (also with JWT tokens)
        API keys in:
            Headers
            Query parameters.
            Cookies, etc.
    Dependency Injection
    Unlimeted "plug-ins"
    Tested
    Starlette Features (another python framework):
        WebSocket support
        GraphQL support
        In-process background tasks
        Startup and shutdown events
        Test client built on requests
        CORS, GZip, Static Files, Streaming responses
        Session and Cookie support
    Other Supports:
        SQL databases
        NoSQL databases
        GraphQL

Getting Started:
    Install and Setup
    Break it down, how it structured
    Basic Concepts:
        Path Parameters
        API Docs - swagger/redocs
        Query parameters
        Request body
    Intermediate Concepts:
        Debugging FastAPI
        Pydantic Schemas
        SqlAlchemy datanase connection
        Models and table
    Database Task:
        Store blog to database
        Get blogs from database
        Delete
        Update
    Responses:
        Handling Exceptions
        Return response
        Define response model
    User and Password
        Create user
        Hash user password
        Show single user
        Define docs tags
    Relationship
        Define User to Blog relationship
        Define blog to user relationship
    Refactor for bigger application
        API Router
        API Router with parameters
    Authentication using JWT
        Create Login route
        Login and verify password
        Return JWT access token
        Routes behind authentication
    Deploy FastAPI
        Using Deta.sh website to deploy
    
    
OpenAPI
    FastAPI generates a "schema" with all your API using the OpenAPI standard for defining APIs.

    "Schema"
    A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.

    API "schema"
    In this case, OpenAPI is a specification that dictates how to define a schema of your API.

    This schema definition includes your API paths, the possible parameters they take, etc.

    Data "schema"
    The term "schema" might also refer to the shape of some data, like a JSON content.

    In that case, it would mean the JSON attributes, and data types they have, etc.

    OpenAPI and JSON Schema
    OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using JSON Schema, the standard for JSON data schemas.

    Check the openapi.json
    If you are curious about how the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API.

What is OpenAPI for
    The OpenAPI schema is what powers the two interactive documentation systems included.

    And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with FastAPI.

    You could also use it to generate code automatically, for clients that communicate with your API. For example, frontend, mobile or IoT applications.

Operation
    "Operation" here refers to one of the HTTP "methods".

    One of:

    POST
    GET
    PUT
    DELETE
    ...and the more exotic ones:

    OPTIONS
    HEAD
    PATCH
    TRACE
    In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".

    When building APIs, you normally use these specific HTTP methods to perform a specific action.

    Normally you use:

    POST: to create data.
    GET: to read data.
    PUT: to update data.
    DELETE: to delete data.
    So, in OpenAPI, each of the HTTP methods is called an "operation".

    We are going to call them "operations" too.

Define a path operation decorator
    The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

        the path /
        using a get operation

    You can also use the other operations:

        @app.post()
        @app.put()
        @app.delete()
        And the more exotic ones:

        @app.options()
        @app.head()
        @app.patch()
        @app.trace()

Return the content

    You can return a dict, list, singular values as str, int, etc.

    You can also return Pydantic models (you'll see more about that later).

    There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.

Recap
    Import FastAPI.
    Create an app instance.
    Write a path operation decorator using decorators like @app.get("/").
    Define a path operation function; for example, def root(): ....
    Run the development server using the command fastapi dev.


Path Parameters
   You can declare path "parameters" or "variables" with the same syntax used by Python format strings.
   You can declare the type of a path parameter in the function, using standard Python type annotations.

Data conversion
Data validation

    So, with the same Python type declaration, FastAPI gives you data validation.

    Notice that the error also clearly states exactly the point where the validation didn't pass.

    This is incredibly helpful while developing and debugging code that interacts with your API.

Pydantic
All the data validation is performed under the hood by Pydantic, so you get all the benefits from it. And you know you are in good hands.

You can use the same type declarations with str, float, bool and many other complex data types.

Several of these are explored in the next chapters of the tutorial.

Order matters
    When creating path operations, you can find situations where you have a fixed path.

    Like /users/me, let's say that it's to get data about the current user.

    And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.

    Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}

    Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".

Predefined values
    If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.

Create an Enum class
    
    Apart: An Enum (short for enumeration) is a class in Python that allows defining a set of named constant values. It is useful when you want to represent a fixed set of possible values, making your code more readable and less error-prone.
    Example:
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        print(Color.RED)       # Output: Color.RED
        print(Color.RED.value) # Output: 1
        print(Color.GREEN)     # Output: Color.GREEN

    Import Enum and create a sub-class that inherits from str and from Enum.

    By inheriting from str the API docs will be able to know that the values must be of type string and will be able to render correctly.

    Then create class attributes with fixed values, which will be the available valid values

    Then create a path parameter with a type annotation using the enum class you created

    You can compare it with the enumeration member in your created enum
    You can get the actual value (a str in this case) using model_name.value, or in general, your_enum_member.value
    Return enumeration members
        You can return enum members from your path operation, even nested in a JSON body (e.g. a dict).
        They will be converted to their corresponding values (strings in this case) before returning them to the client:

Path parameters containing paths
    Let's say you have a path operation with a path /files/{file_path}.

    But you need file_path itself to contain a path, like home/johndoe/myfile.txt.

    So, the URL for that file would be something like: /files/home/johndoe/myfile.txt.

OpenAPI support
    OpenAPI doesn't support a way to declare a path parameter to contain a path inside, as that could lead to scenarios that are difficult to test and define.

    Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette.

    And the docs would still work, although not adding any documentation telling that the parameter should contain a path.

Path convertor
    Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:

    /files/{file_path:path}
    In this case, the name of the parameter is file_path, and the last part, :path, tells it that the parameter should match any path.

Recap
    With FastAPI, by using short, intuitive and standard Python type declarations, you get:
        Editor support: error checks, autocompletion, etc.
        Data "parsing"
        Data validation
        API annotation and automatic documentation
        And you only have to declare them once.
        That's probably the main visible advantage of FastAPI compared to alternative frameworks (apart from the raw performance).

Query Parameters:
    When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
    All the same process that applied for path parameters also applies for query parameters.
    As query parameters are not a fixed part of a path, they can be optional and can have default values.
    You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which. And you don't have to declare them in any specific order. They will be detected by name.
    When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.cIf you don't want to add a specific value but just make it optional, set the default as None. But when you want to make a query parameter required, you can just not declare any default value.
    And of course, you can define some parameters as required, some as having a default value, and some entirely optional.
    