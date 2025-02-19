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

Request Body:
    When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.
    A request body is data sent by the client to your API. A response body is the data your API sends to the client.
    Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.
    To declare a request body, you use Pydantic models with all their power and benefits.
    Info:
    To send data, you should use one of: POST (the more common), PUT, DELETE or PATCH.
    Sending a body with a GET request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.
    As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using GET, and proxies in the middle might not support it.

    Import Pydantic's BaseModel
        First, you need to import BaseModel from pydantic.
        Create your data model. Then you declare your data model as a class that inherits from BaseModel. Use standard Python types for all the attributes.
        The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use None to make it just optional.
        To add it to your path operation, declare it the same way you declared path and query parameters... and declare its type as the model you created.
        Results:
            With just that Python type declaration, FastAPI will:
            Read the body of the request as JSON.
            Convert the corresponding types (if needed).
            Validate the data.
            If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
            Give you the received data in the parameter item.
            As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
            Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
            Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.
    Request body + path parameters
        You can declare path parameters and request body at the same time.
        FastAPI will recognize that the function parameters that match path parameters should be taken from the path, and that function parameters that are declared to be Pydantic models should be taken from the request body.
    Request body + path + query parameters
        You can also declare body, path and query parameters, all at the same time.
        FastAPI will recognize each of them and take the data from the correct place.
        The function parameters will be recognized as follows:
            If the parameter is also declared in the path, it will be used as a path parameter.
            If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
            If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

    FastAPI will know that the value of q is not required because of the default value = None.
    The str | None (Python 3.10+) or Union in Union[str, None] (Python 3.8+) is not used by FastAPI to determine that the value is not required, it will know it's not required because it has a default value of = None.
    But adding the type annotations will allow your editor to give you better support and detect errors.

    Without Pydantic
    If you don't want to use Pydantic models, you can also use Body parameters. See the docs for Body - Multiple Parameters: Singular values in body: 
        Singular values in body
            The same way there is a Query and Path to define extra data for query and path parameters, FastAPI provides an equivalent Body.
            For example, extending the previous model, you could decide that you want to have another key importance in the same body, besides the item and user.
            If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.
            But you can instruct FastAPI to treat it as another body key using Body:


Query parameters and String Validations:
    FastAPI allows you to declare additional information and validation for your parameters.
    Additional validation:
        To achieve that, first import:
            Query from fastapi
            Annotated from typing
        What we will do is wrap that with Annotated, so it becomes: q: str | None = None
        q is a parameter that can be a str or None, and by default, it is None.
        Now that we have this Annotated where we can put more information (in this case some additional validation), add Query inside of Annotated, and set the parameter max_length.
        Here we are using Query() because this is a query parameter. Later we will see others like Path(), Body(), Header(), and Cookie(), that also accept the same arguments as Query().
    FastAPI will now:
        Validate the data making sure the max length.
        Show a clear error for the client when the data is not valid.
        Document the parameter in the OpenAPI schema path operation (so it will show up in the automatic docs UI).
    Advantages of Annotated:
        Using Annotated is recommended instead of the default value in function parameters, it is better for multiple reasons.
        The default value of the function parameter is the actual default value, that's more intuitive with Python in general.
        You could call that same function in other places without FastAPI, and it would work as expected. If there's a required parameter (without a default value), your editor will let you know with an error, Python will also complain if you run it without passing the required parameter.
        When you don't use Annotated and instead use the (old) default value style, if you call that function without FastAPI in other places, you have to remember to pass the arguments to the function for it to work correctly, otherwise the values will be different from what you expect (e.g. QueryInfo or something similar instead of str). And your editor won't complain, and Python won't complain running that function, only when the operations inside error out.
        Because Annotated can have more than one metadata annotation, you could now even use the same function with other tools, like Typer.
    We can use more than one validation and also we can validate a regular expression.
    We can use a default value different than None. Having a default value of any type, including None, makes the parameter optional (not required).
    When you need to declare a value as required while using Query, you can simply not declare a default value.
    We can set None as a required type. We can declare that a parameter can accept None, but that it's still required. This would force clients to send a value, even if the value is None. To do that, we can declare that None is a valid type but simply do not declare a default value.
    When you define a query parameter explicitly with Query you can also declare it to receive a list of values, or said in another way, to receive multiple values. To declare a query parameter with a type of list, you need to explicitly use Query, otherwise it would be interpreted as a request body.
    We can also use list without declaring its type. Keep in mind that in this case, FastAPI won't check the contents of the list.
    For example, list[int] would check (and document) that the contents of the list are integers. But list alone wouldn't.
    Declare more metadata:
        You can add more information about the parameter.
        That information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools. Keep in mind that different tools might have different levels of OpenAPI support. Some of them might not show all the extra information declared yet, although in most of the cases, the missing feature is already planned for development.
    Alias parameters:
        Imagine that you want the parameter to be item-query.
        Like in: http://127.0.0.1:8000/items/?item-query=foobaritems
        But item-query is not a valid Python variable name. The closest would be item_query. But you still need it to be exactly item-query...
        Then you can declare an alias, and that alias is what will be used to find the parameter value.
    Deprecating parameters:
        Now let's say you don't like this parameter anymore.
        You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.
        Then pass the parameter deprecated=True to Query.
    Exclude parameters from OpenAPI:
        To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter include_in_schema of Query to False.
    Recap:
        You can declare additional validations and metadata for your parameters.
        Generic validations and metadata:
            alias
            title
            description
            deprecated
        Validations specific for strings:
            min_length
            max_length
            pattern
        In these examples you saw how to declare validations for str values.


Path Parameters and Numeric Validations:
    In the same way that you can declare more validations and metadata for query parameters with Query, you can declare the same type of validations and metadata for path parameters with Path.
    First, import Path from fastapi, and import Annotated.
    You can declare all the same parameters as for Query.
    A path parameter is always required as it has to be part of the path. Even if you declared it with None or set a default value, it would not affect anything, it would still be always required.
    Order the parameters as you need: This is probably not as important or necessary if you use Annotated.
        Let's say that you want to declare the query parameter q as a required str.
        And you don't need to declare anything else for that parameter, so you don't really need to use Query.
        But you still need to use Path for the item_id path parameter. And you don't want to use Annotated for some reason.
        Python will complain if you put a value with a "default" before a value that doesn't have a "default".
        But you can re-order them, and have the value without a default (the query parameter q) first.
        It doesn't matter for FastAPI. It will detect the parameters by their names, types and default declarations (Query, Path, etc), it doesn't care about the order.
        But keep in mind that if you use Annotated, you won't have this problem, it won't matter as you're not using the function parameter default values for Query() or Path().
    Order the parameters as you need, tricks: This is probably not as important or necessary if you use Annotated.
        Here's a small trick that can be handy, but you won't need it often.
        If you want to:
            declare the q query parameter without a Query nor any default value
            declare the path parameter item_id using Path
            have them in a different order
            not use Annotated
            ...Python has a little special syntax for that.
                Pass *, as the first parameter of the function.
                Python won't do anything with that *, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
            Better with Annotated. Keep in mind that if you use Annotated, as you are not using function parameter default values, you won't have this problem, and you probably won't need to use *.

    Number validations: greater than or equal:
        With Query and Path (and others you'll see later) you can declare number constraints.
        Here, with ge=1, item_id will need to be an integer number "greater than or equal" to 1.
        Number validations also work for float values.
            Here's where it becomes important to be able to declare gt and not just ge. As with it you can require, for example, that a value must be greater than 0, even if it is less than 1.
            So, 0.5 would be a valid value. But 0.0 or 0 would not.
            And the same for lt.

    Recap:
        With Query, Path (and others you haven't seen yet) you can declare metadata and string validations in the same ways as with Query Parameters and String Validations.
        And you can also declare numeric validations:
            gt: greater than
            ge: greater than or equal
            lt: less than
            le: less than or equal
        Query, Path, and other classes you will see later are subclasses of a common Param class.
        All of them share the same parameters for additional validation and metadata you have seen.
        When you import Query, Path and others from fastapi, they are actually functions.
        That when called, return instances of classes of the same name.
        So, you import Query, which is a function. And when you call it, it returns an instance of a class also named Query.
        These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.
        That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.