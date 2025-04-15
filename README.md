# python_web_framework_fastapi
Youtube course from Bitfumes

Installation:
    pip install "fastapi[standard]"
Run:
    fastapi dev main.py
Run with Uvicorn:
    uvicorn file_name:app_name --reload

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


Query Parameter Model:
    If you have a group of query parameters that are related, you can create a Pydantic model to declare them.
    This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once.
    Declare the query parameters that you need in a Pydantic model, and then declare the parameter as Query.
    FastAPI will extract the data for each field from the query parameters in the request and give you the Pydantic model you defined.
    Forbid Extra Query Parameters:
        In some special use cases (probably not very common), you might want to restrict the query parameters that you want to receive.
        You can use Pydantic's model configuration to forbid any extra fields.
        If a client tries to send some extra data in the query parameters, they will receive an error response.
    Spoiler alert: you can also use Pydantic models to declare cookies and headers, but you will read about that later in the tutorial.


Body - Multiple Parameters:
    Now that we have seen how to use Path and Query, let's see more advanced uses of request body declarations.
    Mix Path, Query and body parameters:
        First, of course, you can mix Path, Query and request body parameter declarations freely and FastAPI will know what to do. And you can also declare body parameters as optional, by setting the default to None.
    Multiple body parameters:
        We can also declare multiple body parameters. Like to classes from Pydantic Model.
        So, it will then use the parameter names as keys (field names) in the body.
    Singular values in body:
        The same way there is a Query and Path to define extra data for query and path parameters, FastAPI provides an equivalent Body. For example, you could decide that you want to have another key in the same body.
        If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.
        But you can instruct FastAPI to treat it as another body key using Body.
    Multiple body params and query:
        Of course, you can also declare additional query parameters whenever you need, additional to any body parameters. As, by default, singular values are interpreted as query parameters, you don't have to explicitly add a Query.
    Embed a single body parameter:
        Body also has all the same extra validation and metadata parameters as Query,Path and others you will see later.
        Let's say you only have a single item body parameter from a Pydantic model Item.
        By default, FastAPI will then expect its body directly.
        But if you want it to expect a JSON with a key item and inside of it the model contents, as it does when you declare extra body parameters, you can use the special Body parameter embed: item: Item = Body(embed=True).
    Recap:
        You can add multiple body parameters to your path operation function, even though a request can only have a single body.
        But FastAPI will handle it, give you the correct data in your function, and validate and document the correct schema in the path operation.
        You can also declare singular values to be received as part of the body.
        And you can instruct FastAPI to embed the body in a key even when there is only a single parameter declared.



Body - Fields:
    The same way you can declare additional validation and metadata in path operation function parameters with Query, Path and Body, you can declare validation and metadata inside of Pydantic models using Pydantic's Field. Field works the same way as Query, Path and Body, it has all the same parameters, etc. This extra information will be included in the generated JSON schema.
    We need to import Field from pydantic
    Technical details:
        Actually, Query, Path and others you'll see next create objects of subclasses of a common Param class, which is itself a subclass of Pydantic's FieldInfo class.
        And Pydantic's Field returns an instance of FieldInfo as well.
        Body also returns objects of a subclass of FieldInfo directly. And there are others you will see later that are subclasses of the Body class.
        Remember that when you import Query, Path, and others from fastapi, those are actually functions that return special classes.
        Notice how each model's attribute with a type, default value and Field has the same structure as a path operation function's parameter, with Field instead of Path, Query and Body.
        Extra keys passed to Field will also be present in the resulting OpenAPI schema for your application. As these keys may not necessarily be part of the OpenAPI specification, some OpenAPI tools, for example the OpenAPI validator, may not work with your generated schema.
    Recap:
        You can use Pydantic's Field to declare extra validations and metadata for model attributes.
        You can also use the extra keyword arguments to pass additional JSON Schema metadata.

Body - Nested Models:
    With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).
    List fields:
        You can define an attribute to be a subtype.
    List fields with type parameter:
       Python has a specific way to declare lists with internal types, or "type parameters".
       In Python 3.9 and above you can use the standard list to declare these type annotations.
       But in Python versions before 3.9 (3.6 and above), you first need to import List from standard Python's typing module.
       That's all standard Python syntax for type declarations. Use that same standard syntax for model attributes with internal types.
    Set types:
        But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.
        And Python has a special data type for sets of unique items, the set.
        Then we can declare tags as a set of strings.
        With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.
    Nested Models:
        Each attribute of a Pydantic model has a type.
        But that type can itself be another Pydantic model.
        So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.
        All that, arbitrarily nested.
        Again, doing just that declaration, with FastAPI you get:
            Editor support (completion, etc.), even for nested models.
            Data conversion.
            Data validation.
            Automatic documentation.
    Special types and validation:
        Apart from normal singular types like str, int, float, etc. you can use more complex singular types that inherit from str.
        To see all the options you have, checkout Pydantic's Type Overview.
    Attributes with lists of submodels:
        You can also use Pydantic models as subtypes of list, set, etc.
    Deeply nested models:
        You can define arbitrarily deeply nested models.
    Bodies of pure lists:
        If the top level value of the JSON body you expect is a JSON array (a Python list), you can declare the type in the parameter of the function, the same as in Pydantic models: images: list[Image]
    You couldn't get this kind of editor support if you were working directly with dict instead of Pydantic models.
    But you don't have to worry about them either, incoming dicts are converted automatically and your output is converted automatically to JSON too.
    Bodies of arbitrary dicts:
        You can also declare a body as a dict with keys of some type and values of some other type.
        This way, you don't have to know beforehand what the valid field/attribute names are (as would be the case with Pydantic models).
        This would be useful if you want to receive keys that you don't already know.
        Another useful case is when you want to have keys of another type (e.g., int).
        Keep in mind that JSON only supports str as keys.
        But Pydantic has automatic data conversion.
        This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.
        And the dict you receive as weights will actually have int keys and float values.
    Recap:
        With FastAPI you have the maximum flexibility provided by Pydantic models, while keeping your code simple, short and elegant.But with all the benefits:
            Editor support (completion everywhere!).
            Data conversion (a.k.a. parsing / serialization).
            Data validation.
            Schema documentation.
            Automatic docs.

Declare Request Example Data:
    You can declare examples of the data your app can receive. There are several ways to do it.
    Extra JSON Schema data in Pydantic models:
        That extra info will be added as-is to the output JSON Schema for that model, and it will be used in the API docs.
        In Pydantic version 2, you would use the attribute model_config, that takes a dict as described in Pydantic's docs: Configuration.
        You can set "json_schema_extra" with a dict containing any additional data you would like to show up in the generated JSON Schema, including examples.
        You could use the same technique to extend the JSON Schema and add your own custom extra info. For example you could use it to add metadata for a frontend user interface, etc.
        OpenAPI 3.1.0 (used since FastAPI 0.99.0) added support for examples, which is part of the JSON Schema standard.
        Before that, it only supported the keyword example with a single example. That is still supported by OpenAPI 3.1.0, but is deprecated and is not part of the JSON Schema standard. So you are encouraged to migrate example to examples.
    Field additional arguments:
        When using Field() with Pydantic models, you can also declare additional examples.
    examples in JSON Schema - OpenAPI:
        When using any of:
            Path()
            Query()
            Header()
            Cookie()
            Body()
            Form()
            File()
        You can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.
    Body with examples:
        Here we pass examples containing one example of the data expected in Body().
    Body with multiple examples:
        You can of course also pass multiple examples.
        When you do this, the examples will be part of the internal JSON Schema for that body data.
        Nevertheless, at the time of writing this, Swagger UI, the tool in charge of showing the docs UI, doesn't support showing multiple examples for the data in JSON Schema. But read below for a workaround.
    Using the openapi_examples Parameter:
        You can declare the OpenAPI-specific examples in FastAPI with the parameter openapi_examples for:
            Path()
            Query()
            Header()
            Cookie()
            Body()
            Form()
            File()
        The keys of the dict identify each example, and each value is another dict.
        Each specific example dict in the examples can contain:
            summary: Short description for the example.
            description: A long description that can contain Markdown text.
            value: This is the actual example shown, e.g. a dict.
            externalValue: alternative to value, a URL pointing to the example. Although this might not be supported by as many tools as value.

Extra Data Types:
    Up to now, you have been using common data types, like:
        int
        float
        str
        bool
    But you can also use more complex data types. And you will still have the same features as seen up to now:
        Great editor support.
        Data conversion from incoming requests.
        Data conversion for response data.
        Data validation.
        Automatic annotation and documentation.
    Other data types:
        Here are some of the additional data types you can use:
            UUID:
                A standard "Universally Unique Identifier", common as an ID in many databases and systems.
                In requests and responses will be represented as a str.
            datetime.datetime:
                A Python datetime.datetime.
                In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.
            datetime.date:
                Python datetime.date.
                In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.
            datetime.time:
                A Python datetime.time.
                In requests and responses will be represented as a str in ISO 8601 format, like: 14:23:55.003.
            datetime.timedelta:
                A Python datetime.timedelta.
                In requests and responses will be represented as a float of total seconds.
                Pydantic also allows representing it as a "ISO 8601 time diff encoding", see the docs for more info.
            frozenset:
                In requests and responses, treated the same as a set:
                In requests, a list will be read, eliminating duplicates and converting it to a set.
                In responses, the set will be converted to a list.
                The generated schema will specify that the set values are unique (using JSON Schema's uniqueItems).
            bytes:
                Standard Python bytes.
                In requests and responses will be treated as str.
                The generated schema will specify that it's a str with binary "format".
            Decimal:
                Standard Python Decimal.
                In requests and responses, handled the same as a float.
            You can check all the valid Pydantic data types here: Pydantic data types.

Cookie Parameters:
    First: What is a Cokkie?
            A cookie is a small piece of data stored on a user's browser by a website. It helps websites remember information about users, such as loging status, preferences, and tracking data.
        Some types of Cookies:
            Session Cookies: stored temporarily in the browser and deleted when the user closes the browser. Example: keeping a user logged while they navigate pages.
            Persistent Cookies: stored for a longer period, even after closing the browser. Example: "remember me" login feature.
            First-Party Cookies: created by the website the user is visiting. Example: language preferences on a website.
            Third-Party Cookies: created by domains other than the one being visited (often used for traking and advertising). Example: Ads tracking user behaibor across different websites.
        How Cookies work:
            A user visits a website.
            The website sends a cookie to the user's browser.
            The browser stores the cookie.
            On future visits, the browser sends the cookie back to the website.
    Cookie Parameters:
        You can define Cookie parameters the same way you define Query and Path parameters. First import Cookie.
    Declare Cookie Parameters:
        Then declare the cookie parameters using the same structure as with Path and Query.
        You can define the default value as well as all the extra validation or annotation parameters.
    Technical Details: (Valid for Header parameters too)
        Cookie is a "sister" class of Path and Query. It also inherits from the same common Param class.
        But remember that when you import Query, Path, Cookie and others from fastapi, those are actually functions that return special classes.
        To declare cookies, you need to use Cookie, because otherwise the parameters would be interpreted as query parameters.
    Recap:
        Declare cookies with Cookie, using the same common pattern as Query and Path.

Header Parameters:
    First: What is a Header?
        A Header is a metadata sent along with HTTP requests and responses. It provides important information about the request/response, such as content type, authentication, caching, and more.
        Types of Headers:
            Request Headers: sent from the client (browser/API) to the server. Example: Authorization, User-Agent, Content-Type.
            Response Headers: sent from the server back to the client. Example: Set-Cookie, Content-Length, Cache-Control.
        Common Headers & Their Purpose:
            Authorization: Used for authentication (e.g., API tokens, Basic Auth).
            Content-Type: Defines the type of data being sent (e.g., application/json).
            User-Agent: Identifies the client making the request (browser, API, etc.).
            Accept: Specifies the data formats the client can process (e.g., text/html).
            Cache-Control: Controls caching behavior.
            Set-Cookie: Used to send cookies from server to client.
    You can define Header parameters the same way you define Query, Path and Cookie parameters. First import Header.
    Declare Header parameters:
        Then declare the header parameters using the same structure as with Path, Query and Cookie.
        You can define the default value as well as all the extra validation or annotation parameters.
    Automatic conversion:
        Header has a little extra functionality on top of what Path, Query and Cookie provide.
        Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).
        But a variable like user-agent is invalid in Python.
        So, by default, Header will convert the parameter names characters from underscore (_) to hyphen (-) to extract and document the headers.
        Also, HTTP headers are case-insensitive, so, you can declare them with standard Python style (also known as "snake_case").
        So, you can use user_agent as you normally would in Python code, instead of needing to capitalize the first letters as User_Agent or something similar.
        If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter convert_underscores of Header to False. Warning: Before setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.
    Duplicate headers:
        It is possible to receive duplicate headers. That means, the same header with multiple values.
        You can define those cases using a list in the type declaration.
        You will receive all the values from the duplicate header as a Python list.
        If you communicate with that path operation sending two HTTP headers like:
            X-Token: foo
            X-Token: bar
        The response would be like:
            {
                "X-Token values": [
                    "bar",
                    "foo"
                ]
            }
    Recap:
        Declare headers with Header, using the same common pattern as Query, Path and Cookie.
        And don't worry about underscores in your variables, FastAPI will take care of converting them.

Cookie Parameter Models:
    If you have a group of cookies that are related, you can create a Pydantic model to declare them.
    This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once.
    This same technique applies to Query, Cookie, and Header.
    Cookies with a Pydantic Model:
        Declare the cookie parameters that you need in a Pydantic model, and then declare the parameter as Cookie. (Same for Header).
        FastAPI will extract the data for each field from the cookies received in the request and give you the Pydantic model you defined. (Same for Header).
    Info:
        Have in mind that, as browsers handle cookies in special ways and behind the scenes, they don't easily allow JavaScript to touch them.
        If you go to the API docs UI at /docs you will be able to see the documentation for cookies for your path operations.
        But even if you fill the data and click "Execute", because the docs UI works with JavaScript, the cookies won't be sent, and you will see an error message as if you didn't write any values.
    Forbid Extra Cookies: (Same for Header)
        In some special use cases (probably not very common), you might want to restrict the cookies that you want to receive.
        Your API now has the power to control its own cookie consent.
        You can use Pydantic's model configuration to forbid any extra fields.
        If a client tries to send some extra cookies, they will receive an error response.
        Poor cookie banners with all their effort to get your consent for the API to reject it.
        For example, if the client tries to send a santa_tracker cookie with a value of good-list-please, the client will receive an error response telling them that the santa_tracker cookie is not allowed.
    Summary: (Same for Header)
        You can use Pydantic models to declare cookies in FastApi.

Response Model - Return Type
    You can declare the type used for the response by annotating the path operation function return type.
    You can use type annotations the same way you would for input data in function parameters, you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.
    FastAPI will use this return type to:
        Validate the returned data.
            If the data is invalid (e.g. you are missing a field), it means that your app code is broken, not returning what it should, and it will return a server error instead of returning incorrect data. This way you and your clients can be certain that they will receive the data and the data shape expected.
        Add a JSON Schema for the response, in the OpenAPI path operation.
            This will be used by the automatic docs.
            It will also be used by automatic client code generation tools.
        But most importantly:
            It will limit and filter the output data to what is defined in the return type.
            This is particularly important for security, we'll see more of that below.
    response_model Parameter:
        There are some cases where you need or want to return some data that is not exactly what the type declares.
        For example, you could want to return a dictionary or a database object, but declare it as a Pydantic model. This way the Pydantic model would do all the data documentation, validation, etc. for the object that you returned (e.g. a dictionary or database object).
        If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).
        In those cases, you can use the path operation decorator parameter response_model instead of the return type.
        You can use the response_model parameter in any of the path operations:
            @app.get()
            @app.post()
            @app.put()
            @app.delete()
            etc.
        Notice that response_model is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.
        response_model receives the same type you would declare for a Pydantic model field, so, it can be a Pydantic model, but it can also be, e.g. a list of Pydantic models, like List[Item].
        FastAPI will use this response_model to do all the data documentation, validation, etc. and also to convert and filter the output data to its type declaration.
        If you have strict type checks in your editor, mypy, etc, you can declare the function return type as Any.
        That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data documentation, validation, filtering, etc. with the response_model.
    response_model Priority:
        If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.
        This way you can add correct type annotations to your functions even when you are returning a type different than the response model, to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the response_model.
        You can also use response_model=None to disable creating a response model for that path operation, you might need to do it if you are adding type annotations for things that are not valid Pydantic fields, you will see an example of that in one of the sections below.
    Return the same input data:
        Example in main: Now, whenever a browser is creating a user with a password, the API will return the same password in the response.
        In this case, it might not be a problem, because it's the same user sending the password.
        But if we use the same model for another path operation, we could be sending our user's passwords to every client.
        Danger: Never store the plain password of a user or send it in a response like this, unless you know all the caveats and you know what you are doing.
    Add an output model: (base on the example)
        Here, even though our path operation function is returning the same input user that contains the password ...we declared the response_model to be our model UserOut, that doesn't include the password.
        So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).
    response_model or Return Type:
        In this case, because the two models are different, if we annotated the function return type as UserOut, the editor and tools would complain that we are returning an invalid type, as those are different classes.
        That's why in this example we have to declare it in the response_model parameter.
        ...but continue reading below to see how to overcome that.
    Return Type and Data Filtering:
        Let's continue from the previous example. We wanted to annotate the function with one type, but we wanted to be able to return from the function something that actually includes more data.
        We want FastAPI to keep filtering the data using the response model. So that even though the function returns more data, the response will only include the fields declared in the response model.
        In the previous example, because the classes were different, we had to use the response_model parameter. But that also means that we don't get the support from the editor and tools checking the function return type.
        But in most of the cases where we need to do something like this, we want the model just to filter/remove some of the data as in this example.
        And in those cases, we can use classes and inheritance to take advantage of function type annotations to get better support in the editor and tools, and still get the FastAPI data filtering.
        With this, we get tooling support, from editors and mypy as this code is correct in terms of types, but we also get the data filtering from FastAPI.
        How does this work? Let's check that out:
            Type Annotations and Tooling:
                First let's see how editors, mypy and other tools would see this.
                BaseUser has the base fields. Then UserIn inherits from BaseUser and adds the password field, so, it will include all the fields from both models.
                We annotate the function return type as BaseUser, but we are actually returning a UserIn instance.
                The editor, mypy, and other tools won't complain about this because, in typing terms, UserIn is a subclass of BaseUser, which means it's a valid type when what is expected is anything that is a BaseUser.
            FastAPI Data Filtering:
                Now, for FastAPI, it will see the return type and make sure that what you return includes only the fields that are declared in the type.
                FastAPI does several things internally with Pydantic to make sure that those same rules of class inheritance are not used for the returned data filtering, otherwise you could end up returning much more data than what you expected.
                This way, you can get the best of both worlds: type annotations with tooling support and data filtering.
            See it in the docs:
                When you see the automatic docs, you can check that the input model and output model will both have their own JSON Schema. And both models will be used for the interactive API documentation.
    Other Return Type Annotation:
        There might be cases where you return something that is not a valid Pydantic field and you annotate it in the function, only to get the support provided by tooling (the editor, mypy, etc).
        Return a Response Directly:
            The most common case would be returning a Response directly as explained later in the advanced docs.
            This simple case is handled automatically by FastAPI because the return type annotation is the class (or a subclass of) Response.
            And tools will also be happy because both RedirectResponse and JSONResponse are subclasses of Response, so the type annotation is correct.
        Annotate a Response Subclass
            You can also use a subclass of Response in the type annotation.
            This will also work because RedirectResponse is a subclass of Response, and FastAPI will automatically handle this simple case.
        Invalid Return Type Annotations:
            But when you return some other arbitrary object that is not a valid Pydantic type (e.g. a database object) and you annotate it like that in the function, FastAPI will try to create a Pydantic response model from that type annotation, and will fail.
            The same would happen if you had something like a union between different types where one or more of them are not valid Pydantic types.
            @app.get("/portal")
            async def get_portal(teleport: bool = False) -> Response | dict:
                if teleport:
                    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                return {"message": "Here's your interdimensional portal."}
            ...this fails because the type annotation is not a Pydantic type and is not just a single Response class or subclass, it's a union (any of the two) between a Response and a dict
        Disable Response Model:
            Continuing from the example above, you might not want to have the default data validation, documentation, filtering, etc. that is performed by FastAPI.
            But you might want to still keep the return type annotation in the function to get the support from tools like editors and type checkers (e.g. mypy).
            In this case, you can disable the response model generation by setting response_model=None.
            This will make FastAPI skip the response model generation and that way you can have any return type annotations you need without it affecting your FastAPI application.
    Response Model encoding parameters:
        Your response model could have default values.
        But you might want to omit them from the result if they were not actually stored.
        For example, if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values.
        Use the response_model_exclude_unset parameter:
            You can set the path operation decorator parameter response_model_exclude_unset=True
            and those default values won't be included in the response, only the values actually set.
            You can also use:
                response_model_exclude_defaults=True
                response_model_exclude_none=True
        Data with values for fields with defaults:
            But if your data has values for the model's fields with default values, they will be included in the response.
        Data with the same values as the defaults:
            If the data has the same values as the default ones, FastAPI is smart enough (actually, Pydantic is smart enough) to realize that they were set explicitly (instead of taken from the defaults).
            So, they will be included in the JSON response.
    response_model_include and response_model_exclude:
        You can also use the path operation decorator parameters response_model_include and response_model_exclude.
        They take a set of str with the name of the attributes to include (omitting the rest) or to exclude (including the rest).
        This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.
        But it is still recommended to use the ideas above, using multiple classes, instead of these parameters.
        This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for the complete model, even if you use response_model_include or response_model_exclude to omit some attributes.
        This also applies to response_model_by_alias that works similarly.
        Using lists instead of sets:
            If you forget to use a set and use a list or tuple instead, FastAPI will still convert it to a set and it will work correctly (see changes).
    Recap:
        Use the path operation decorator's parameter response_model to define response models and especially to ensure private data is filtered out.
        Use response_model_exclude_unset to return only the values explicitly set.

Extra Models:
    Continuing with the previous example, it will be common to have more than one related model.
    This is especially the case for user models, because:
        The input model needs to be able to have a password.
        The output model should not have a password.
        The database model would probably need to have a hashed password.
    Multiple models:
        Here's a general idea of how the models could look like with their password fields and the places where they are used.
        About **user_in.dict() in the code (or **user_in.model_dump()):
            user_in is a Pydantic model of class UserIn.
            Pydantic models have a .dict() method that returns a dict with the model's data.
            So, if we create a Pydantic object user_in like:
            user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
            and then we call:
            user_dict = user_in.dict()
            we now have a dict with the data in the variable user_dict (it's a dict instead of a Pydantic model object).
            Unpacking a dict:
                If we take a dict like user_dict and pass it to a function (or class) with **user_dict, Python will "unpack" it. It will pass the keys and values of the user_dict directly as key-value arguments.
                So, continuing with the user_dict from above, writing:
                    UserInDB(**user_dict)
                    would result in something equivalent to:
                        UserInDB(
                            username="john",
                            password="secret",
                            email="john.doe@example.com",
                            full_name=None,
                        )
                    Or more exactly, using user_dict directly, with whatever contents it might have in the future:
                        UserInDB(
                            username = user_dict["username"],
                            password = user_dict["password"],
                            email = user_dict["email"],
                            full_name = user_dict["full_name"],
                        )
            A Pydanteic model from the contents of another:
                As in the example above we got user_dict from user_in.dict(), this code:
                    user_dict = user_in.dict()
                    UserInDB(**user_dict)
                    would be equivalent to:
                        UserInDB(**user_in.dict())
                        ...because user_in.dict() is a dict, and then we make Python "unpack" it by passing it to UserInDB prefixed with **.
                        So, we get a Pydantic model from the data in another Pydantic model.
            Unpacking a dict and extra keywords:
                And then adding the extra keyword argument hashed_password=hashed_password, like in:
                    UserInDB(**user_in.dict(), hashed_password=hashed_password)
                    ...ends up being like:
                        UserInDB(
                            username = user_dict["username"],
                            password = user_dict["password"],
                            email = user_dict["email"],
                            full_name = user_dict["full_name"],
                            hashed_password = hashed_password,
                        )
        Reduce duplicarion:
            Reducing code duplication is one of the core ideas in FastAPI.
            As code duplication increments the chances of bugs, security issues, code desynchronization issues (when you update in one place but not in the others), etc.
            And these models are all sharing a lot of the data and duplicating attribute names and types.
            We could do better.
            We can declare a UserBase model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).
            All the data conversion, validation, documentation, etc. will still work as normally.
            That way, we can declare just the differences between the models (with plaintext password, with hashed_password and without password).
    Union or anyOf:
        You can declare a response to be the Union of two or more types, that means, that the response would be any of them.
        It will be defined in OpenAPI with anyOf.
        Note: When defining a Union, include the most specific type first, followed by the less specific type. In the example below, the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].
        To do that, use the standard Python type hint typing.Union.
        Union in Python 3.10:
            In this example we pass Union[PlaneItem, CarItem] as the value of the argument response_model.
            Because we are passing it as a value to an argument instead of putting it in a type annotation, we have to use Union even in Python 3.10.
            If it was in a type annotation we could have used the vertical bar, as:
                some_variable: PlaneItem | CarItem
            But if we put that in the assignment response_model=PlaneItem | CarItem we would get an error, because Python would try to perform an invalid operation between PlaneItem and CarItem instead of interpreting that as a type annotation.
    List of models:
        The same way, you can declare responses of lists of objects.
        For that, use the standard Python typing.List (or just list in Python 3.9 and above).
    Response with arbitrary dict:
        You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values, without using a Pydantic model.
        This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.
        In this case, you can use typing.Dict (or just dict in Python 3.9 and above).
    Recap:
        Use multiple Pydantic models and inherit freely for each case.
        You don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including password, password_hash and no password.

Response Status Code:
    The same way you can specify a response model, you can also declare the HTTP status code used for response with parameter status_code in any of the path operations:
        @app.get()
        @app.post()
        @app.delete()
        @app.put()
        etc.
    Important: Notice that status_code is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.
    The status_code parameter recieves a number with the HTTP status code. (There is a python library for http).
    It will:
        Return that status code in the response.
        Document it as such in the OpenAPI schema (and so, in the user interfaces).
    Note: Some response codes (see the next section) indicate that the response does not have a body.
    FastAPI knows this, and will produce OpenAPI docs that state there is no response body.
    About HTTP status codes:
        In HTTP, you send a numeric status code of 3 digits as part of the response.
        These status codes have a name associated to recognize them, but the important part is the number.
        In short:
            100 - 199 are for "Information". You rarely use them directly. Responses with these status codes cannot have a body.
            200 - 299 are for "Successful" responses. These are the ones you would use the most.
            200 is the default status code, which means everything was "OK".
            Another example would be 201, "Created". It is commonly used after creating a new record in the database.
            A special case is 204, "No Content". This response is used when there is no content to return to the client, and so the response must not have a body.
            300 - 399 are for "Redirection". Responses with these status codes may or may not have a body, except for 304, "Not Modified", which must not have one.
            400 - 499 are for "Client error" responses. These are the second type you would probably use the most.
            An example is 404, for a "Not Found" response.
            For generic errors from the client, you can just use 400.
            500 - 599 are for server errors. You almost never use them directly. When something goes wrong at some part in your application code, or server, it will automatically return one of these status codes.
    Shortcut to remember the names:
        You don't have to memorize what each of the status code mean.
        You can use the convenience variables from fastapi.status.
        They are just a convenience, they hold the same number, but that way you can use the editor's autocomplete to find them.
    Changing the default:
        Later, in the Advanced User Guide, you will see how to return a different status code than the default you are declaring here.

Form Data:
    When you need to recive form fields instead of JSON, you can use Form.
    To use forms, first install python-multipart.
    Import Form from fastapi.
    Define Form parameters:
        Create form parameters the same way you would for Body or Query.
        For example, in one of the ways the OAuth2 specification can be used (called "password flow") it is required to send a username and password as form fields.
        The specification requires the fields to be exactly named username and password, and to be sent as form fields, not JSON.
        With Form you can declare the same configurations as with Body (and Query, Path, Cookie), including validation, examples, an alias (e.g. user-name instead of username), etc.
    Info: Form is a class that inherits directly from Body.
    Tip: To declare form bodies, you need to use Form explicitly, because without it the parameters would be interpreted as query parameters or body (JSON) parameters.
    About "Form Fields":
        The wat HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.
        Technical details: Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded.
        But when the form includes files, it is encoded as multipart/form-data. You'll read about handling files in the next chapter.
        If you want to read more about these encodings and form fields, head to the MDN web docs for POST.
    Warning: You can declare multiple Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using application/x-www-form-urlencoded instead of application/json.
    This is not a limitation of FastAPI, it's part of the HTTP protocol.
    Recap:
        Use Form to declare form data input parameters.

Form Models:
    We can use Pydantic models to declare form fields in FastAPI.
    Pydantic Models for Forms:
        You just need to declare a Pydantic model with the fields you want to receive as form fields, and then declare the parameter as Form.
        FastAPI will extract the data for each field from the form data in the request and give you the Pydantic model you defined.
    Forbid Extra Form Fields:
        In some special cases (probably not very common), you might want to restrict the form fields to only those declared in the Pydantic model. And forbid any extra fields.
        If a client tries to send somo extra data, they will receive an error response.
    Summary:
        You can use Pydantic models to declare form fields in FastAPI.

Request Files:
    You can define files to be uploaded by the client using File.
    First import File and UploadFile from fastapi.
    Define File Parameters:
        Create file parameters the same way you would for Body or Form.
        Info: File is a class that inherits directly from Form.
        To declare File bodies, you need to use File, because otherwise the parameters would be interpreted as query parameters or body (JSON) parameters.
    The files will be uploaded as "form data".
    If you declare the type of your path operation function parameter as bytes, FastAPI will read the file for you and you will receive the contents as bytes.
    Keep in mind that this means that the hole contents will be stored in memory. This will work well for small files.
    But there are several cases in which you might benefit from using UploadFile.
    File Parameters with UploadFile:
        Define a file parameter with a type of UploadFile.
        Using UploadFile has several adventages over bytes:
            You don't have to use File() in the default value of the parameter.
            It uses a "spooled" file:
                A file stored in memory up to maximum size limit, and after passing this limit it will be stored in disk.
            This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.
            You can get metadata from the uploaded file.
            It has a file-like async interface.
            It exposes an actual Python SpooledTemporaryFile object that you can pass directly to other libraries that expect a file-like object.
        UploadFile has the following attributes:
            filename: A str with the original file name that was uploaded (e.g. myimage.jpg).
            content_type: A str with the content type (MIME type / media type) (e.g. image/jpeg).
            file: A SpooledTemporaryFile (a file-like object). This is the actual Python file object that you can pass directly to other functions or libraries that expect a "file-like" object.
        UploadFile has the following async methods. They all call the corresponding file methods underneath (using the internal SpooledTemporaryFile).
            write(data): Writes data (str or bytes) to the file.
            read(size): Reads size (int) bytes/characters of the file.
            seek(offset): Goes to the byte position offset (int) in the file.
            E.g., await myfile.seek(0) would go to the start of the file.
            This is especially useful if you run await myfile.read() once and then need to read the contents again.
            close(): Closes the file.
        As all these methods are async methods, you nedd to"await" them. For example, inside of an async path operation function, 
        you can get the contents with: contents = await myfile.read().
        If you are inside of a normal def path operation function, you can access the UploadFile.file directly: contents = myfile.file.read().
        FastAPI's UploadFile inherits directly from Starlette's UploadFile, but adds some necessary parts to make it compatible with Pydantic and the other parts of FastAPI.
    What is "Form Data":
        The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.
        FastAPI will make sure to read that data from the right place instead of JSON.
        Technocal Details:
            Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded when it doesn't include files.
            But when the form includes files, it is encoded as multipart/form-data. If you use File, FastAPI will know it has to get the files from the correct part of the body.
            If you want to read more about these encodings and form fields, head to the MDN web docs for POST.
        Warning:
            You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead of application/json.
            This is not a limitation of FastAPI, it's part of the HTTP protocol.
    Optional File Upload:
        You can make a file optional by using standard type annotations and setting a default value of None.
    UploadFile with additional metadata:
        You can use File() with UploadFile, for example, to set additional metadata.
    Multiple File Uploads:
        It's possible to upload several files at the same time.
        They would be associated to the same "form field" sent using "form data".
        To use that, declare a list of bytes or UploadFile.
        You will receive, as declared, a lost of bytes or UploadFile's.
    Technocal details:
        You could also use from starlette.responses import HTMLResponse.
        FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.
    Multiple File Uploads with additional metadata:
        And the same way as before, you can use File() to set additional parameters, even for UploadFile.
    Recap:
        Use File, bytes, and, UploadFile to declare files to be uploaded in the request, sent as form data.

Request Forms and Files:
    You can define files and form fields at the same time using File and Form.
    Define File and Form parameters:
        Create file and form parameters the same way you would for Body or Query.
        The files and form fields will be uploaded as form data and you will receive the files and form fields.
        And you can declare some of the files as bytes and some as UploadFile.
    Warning: You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead od application/json. This is not a limitation of FastAPI, it's part of the HTTP protocol.
    Recap:
        Use File and Form together when you need to receive data and files in the same request.


From here on, the code is in main_two.py

Handling Errors:
    There are many situations in which you need to notify an error to a client that is using your API.
    This client could be a browser with a frontend, a code from someone else, an IoT device, etc.
    You could need to tell the client that:
        The client doesn't have enough privileges for that operation.
        The client doesn't have access to that resource.
        The item the client was trying to access doesn't exist.
        etc.
    In these cases, you would normally return an HTTP status code in the range of 400 (from 400 to 499).
    This is similar to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in the request.
    The status codes in the 400 range mean that there was an error from the client.
    Remember all those "404 Not Found" errors (and jokes)?
    Use HTTPException:
        To return HTTP responses with errors to the client you use HTTPException.
        First import HTTPException.
        Raise an HTTPException in your code:
            HTTPException is a normal Python exception with additional data relevant for APIs.
            Because it's a Python exception, you don't return it, you raise it.
            This also means that if you are inside a utility function that you are calling inside of your path operation function, and you raise the HTTPException from inside of that utility function, it won't run the rest of the code in the path operation function, it will terminate that request right away and send the HTTP error from the HTTPException to the client.
            The benefit of raising an exception over returning a value will be more evident in the section about Dependencies and Security.
            Tip (in fastapi): When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail, not only str. You could pass a dict, a list, etc. They are handled automatically by FastAPI and converted to JSON. 
    Add custom headers:
        There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.
        You probably won't need to use it directly in your code.
        But in case you needed it for an advanced scenario, you can add custom headers.
    Install custom exception handlers:
        First import Request and JSONResponse from fastapi.
        You can add custom exception handlers with the same exception utilities from Starlette.
        Let's say you have a custom exception UnicornException that you (or a library you use) might raise.
        And you want to handle this exception globally with FastAPI.
        You could add a custom exception handler with @app.exception_handler() (This is an special decorator).
        Tachnical details: You could also use from starlette.requests import Request and from starlette.responses import JSONResponse.
        FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with Request.
    Override the default exception handlers:
        FastAPI has some default exception handlers.
        These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.
        You can override these exception handlers with your own.
        Override request validation exceptions:
            When a request contains invalid data, FastAPI internally raises a RequestValidationError.
            And it also includes a default exception handler for it.
            To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError) to decorate the exception handler.
            The exception handler will receive a Request and the exception.
            RequestValidationError vs ValidationError:
                FastAPI uses it so that, if you use a Pydantic model in response_model, and your data has an error, you will see the error in your log.
                But the client/user will not see it. Instead, the client will receive an "Internal Server Error" with an HTTP status code 500.
                It should be this way because if you have a Pydantic ValidationError in your response or anywhere in your code (not in the client's request), it's actually a bug in your code.
                And while you fix it, your clients/users shouldn't have access to internal information about the error, as that could expose a security vulnerability.
            Override the HTTPException error handler:
                The same way, you can override the HTTPException handler.
                For example, you could want to return a plain text response instead of JSON for these errors.
                Technical details: You could also use from starlette.responses import PlainTextResponse.
                FastAPI provides the same starlette.responses as fastapi.responses just as a convenience for you, the developer. But most of the available responses come directly from Starlette.
            Use the RequestValidationError body:
                The RequestValidationError contains the body it received with invalid data.
                You could use it while developing your app to log the body and debug it, return it to the user, etc.
                Now try sending an invalid data, You will receive a response telling you that the data is invalid containing the received body.
                FastAPI's HTTPException vs Starlette's HTTPException:
                    FastAPI has its own HTTPException.
                    And FastAPI's HTTPException error class inherits from Starlette's HTTPException error class.
                    The only difference is that FastAPI's HTTPException accepts any JSON-able data for the detail field, while Starlette's HTTPException only accepts strings for it.
                    So, you can keep raising FastAPI's HTTPException as normally in your code.
                    But when you register an exception handler, you should register it for Starlette's HTTPException.
                    This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette HTTPException, your handler will be able to catch and handle it.
                    In this example, to be able to have both HTTPExceptions in the same code, Starlette's exceptions is renamed to StarletteHTTPException.
    Reuse FastAPI's exception handlers:
        If you want to use the exception along with the same default exception handlers from FastAPI, you can import and reuse the default exception handlers from fastapi.exception_handlers.
        In this example you are just printing the error with a very expressive message, but you get the idea. You can use the exception and then just reuse the default exception handlers.

Path Operation Configuration:
    There are several parameters that you can pass to your path operation decorator to configure it.
    Notice that these parameters are passed directly to the path operation decorator, not to your path operation function.
    Response Status Code:
        You can define the (HTTP) status_code to be used in the response of your path operation.
        You can pass directly the int code, like 404.
        But if you don't remember what each number code is for, you can use the shortcut constants in status.
        That status code will be used in the response and will be added to the OpenAPI schema.
    Tags:
        You can add tags to your path operation, pass the parameter tags with a list of str (commonly just one str).
        They will be added to the OpenAPI schema and used by the automatic documentation interfaces.
    Tags with Enums:
        If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.
        In these cases, it could make sense to store the tags in an Enum.
        FastAPI supports that the same way as with plain strings.
    Summary and description:
        You can add a summary and description.
    Description from docstring:
        As descriptions tend to be long and cover multiple lines, you can declare the path operation description in the function docstring and FastAPI will read it from there.
        You can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).
    Response description:
        You can specify the response description with the parameter response_description.
        Notice that response_description refers specifically to the response, the description refers to the path operation in general.
        OpenAPI specifies that each path operation requires a response description.
        So, if you don't provide one, FastAPI will automatically generate one of "Successful response".
    Deprecate a path operation:
        If you need to mark a path operation as deprecated, but without removing it, pass the parameter deprecated.
    Recap:
        You can cobfigure and add metadata for your operations easily by passing parameters to the path operation decorators.

JSON Compatible Encoder:
    There are some cases where you might need to convert a data type (like Pydantic model) to something compatible with JSON (like a dict, list, etc.).
    For example, if you need to store it in a database.
    For that, FastAPI provides a jsonable_encoder() function.
    Using the jsonable_encoder:
        Let's imagine that you have a database fake_db that only receives JSON compatible data.
        For example, it doesn't receive datetime objects, as those are not compatible with JSON.
        So, a datetime object would have to be converted to a str containing the data in ISO format.
        The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a dict.
        You can use jsonable_encoder for that.
        It receives an object, like a Pydantic model, and returns a JSON compatible version.
    The result of calling it is something that can be encoded with the Python standard json.dumps().
    It doesn't return a large str containing the data in JSON format (as a string). It returns a Python standard data structure (e.g. a dict) with values and sub-values that are all compatible with JSON.
    jsonable_encoder is actually used by FastAPI internally to convert data. But it is useful in many other scenarios.

Body - Updates:
    Update replacing with PUT:
        To update an item you can use the HTTP PUT operation.
        You can use the jsonable_encoder() function to convert the input data to data that can be stored as JSON (e.g. with a NoSQL database). For example, converting datetime to str.
        PUT is used to receive data that should replace the existing data.
        Warning about replacing:
            That means that if you want to update the item bar using PUT with a body containing:
                    {
                        "name": "Barz",
                        "price": 3,
                        "description": None,
                    }
            because it doesn't include the already stored attribute "tax": 20.2, the input model would take the default value of "tax": 10.5.
            And the data would be saved with that "new" tax of 10.5.
    Partial updates with PATCH:
        You can also use the HTTP PATCH operation to partially update data.
        This means that you can send only the data you want to update, leaving the rest intact.
        Note:
            PATCH is less commonly used and known than PUT.
            And many teams use only PUT, even for partial updates.
            You are free to use them however you want, FastAPI doesn't impose any restrictions.
            But this guide shows you, more or less, how they are intended to be used.
    Using Pydantic's exclude_unset parameter:
        If you want to receive partial updates, it's very useful to use the parameter exclude_unset in Pydantic's model's .model_dump(). Like item.model_dump(exclude_unset=True).
        That would generate a dict with only the data that was set when creating the item model, excluding default values.
        Then you can use this to generate a dict with only the data that was set (sent in the request), omitting default values.
        Info:
            In Pydantic v1 the method was called .dict(), it was deprecated (but still supported) in Pydantic v2, and renamed to .model_dump().
            The examples here use .dict() for compatibility with Pydantic v1, but you should use .model_dump() instead if you can use Pydantic v2.

    Using Pydantic's update parameter:
        Now, you can create a copy of the existing model using .model_copy(), and pass the update parameter with a dict containing the data to update.
    Partial updates recap:
        In summary, to apply partial updates you would:
            (Optionally) use PATCH instead of PUT.
            Retrieve the stored data.
            Put that data in a Pydantic model.
            Generate a dict without default values from the input model (using exclude_unset).
                This way you can update only the values actually set by the user, instead of overriding values already stored with default values in your model.
            Create a copy of the stored model, updating its attributes with the received partial updates (using the update parameter).
            Convert the copied model to something that can be stored in your DB (for example, using the jsonable_encoder).
                This is comparable to using the model's .model_dump() method again, but it makes sure (and converts) the values to data types that can be converted to JSON, for example, datetime to str.
            Save the data to your DB.
            Return the updated model.
    Tip:
        You can actually use this same technique with an HTTP PUT operation.
        But the example here uses PATCH because it was created for these use cases.
    Note:
        Notice that the input model is still validated.
        So, if you want to receive partial updates that can omit all the attributes, you need to have a model with all the attributes marked as optional (with default values or None).
        To distinguish from the models with all optional values for updates and models with required values for creation, you can use the ideas described in Extra Models.

Dependencies:
    FastAPI has a very powerful but intuitive Dependency Injection system.
    It is designed to be very simple to use, and to make it very easy for any developer to integrate other components with FastAPI.
    What is "Dependency Injection":
        "Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".
        And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).
        This is very useful when you need to:
            Have shared logic (the same code logic again and again).
            Share database connections.
            Enforce security, authentication, role requirements, etc.
            And many other things...
        All these, while minimizing code repetition.
    First Steps:
        Let's see a very simple example. It will be so simple that it is not very useful, for now.
        But this way we can focus on how the Dependency Injection system works.
        Create a dependency, or "dependable":
            Let's first focus on the dependency.
            It is just a function that can take all the same parameters that a path operation function can take.
            And it has the same shape and structure that all your path operation functions have.
            You can think of it as a path operation function without the "decorator" (without the @app.get("/some-path")).
            And it can return anything you want.
            In this case, this dependency expects:
                An optional query parameter q that is a str.
                An optional query parameter skip that is an int, and by default is 0.
                An optional query parameter limit that is an int, and by default is 100.
            And then it just returns a dict containing those values.
            Declare the dependency, in the "dependant":
                The same way you use Body, Query, etc. with your path operation function parameters, use Depends with a new parameter.
            Although you use Depends in the parameters of your function the same way you use Body, Query, etc, Depends works a bit differently.
            You only give Depends a single parameter.
            This parameter must be something like a function.
            You don't call it directly (don't add the parenthesis at the end), you just pass it as a parameter to Depends().
            And that function takes parameters in the same way that path operation functions do.
            You'll see what other "things", apart from functions, can be used as dependencies in the next chapter.
            Whenever a new request arrives, FastAPI will take care of:
                Calling your dependency ("dependable") function with the correct parameters.
                Get the result from your function.
                Assign that result to the parameter in your path operation function.
            This way you write shared code once and FastAPI takes care of calling it for your path operations.
    Share Annotated dependencies:
        In the examples above, you see that there's a tiny bit of code duplication.
        When you need to use the common_parameters() dependency, you have to write the whole parameter with the type annotation and Depends():
            commons: Annotated[dict, Depends(common_parameters)]
        But because we are using Annotated, we can store that Annotated value in a variable and use it in multiple places.
        Tip:
            This is just standard Python, it's called a "type alias", it's actually not specific to FastAPI.
            But because FastAPI is based on the Python standards, including Annotated, you can use this trick in your code. 
        The dependencies will keep working as expected, and the best part is that the type information will be preserved, which means that your editor will be able to keep providing you with autocompletion, inline errors, etc. The same for other tools like mypy.
        This will be especially useful when you use it in a large code base where you use the same dependencies over and over again in many path operations.
    To async or not to async:
        As dependencies will also be called by FastAPI (the same as your path operation functions), the same rules apply while defining your functions.
        You can use async def or normal def.
        And you can declare dependencies with async def inside of normal def path operation functions, or def dependencies inside of async def path operation functions, etc.
        It doesn't matter. FastAPI will know what to do.
    Integrated with OpenAPI:
        All the request declarations, validations and requirements of your dependencies (and sub-dependencies) will be integrated in the same OpenAPI schema.
        So, the interactive docs will have all the information from these dependencies too.
    Simple usage:
        If you look at it, path operation functions are declared to be used whenever a path and operation matches, and then FastAPI takes care of calling the function with the correct parameters, extracting the data from the request.
        Actually, all (or most) of the web frameworks work in this same way.
        You never call those functions directly. They are called by your framework (in this case, FastAPI).
        With the Dependency Injection system, you can also tell FastAPI that your path operation function also "depends" on something else that should be executed before your path operation function, and FastAPI will take care of executing it and "injecting" the results.
        Other common terms for this same idea of "dependency injection" are:
            resources
            providers
            services
            injectables
            components
    FastAPI plug-ins:
        Integrations and "plug-ins" can be built using the Dependency Injection system. But in fact, there is actually no need to create "plug-ins", as by using dependencies it's possible to declare an infinite number of integrations and interactions that become available to your path operation functions.
        And dependencies can be created in a very simple and intuitive way that allows you to just import the Python packages you need, and integrate them with your API functions in a couple of lines of code, literally.
        You will see examples of this in the next chapters, about relational and NoSQL databases, security, etc.
    FastAPI compatibility:
        The simplicity of the dependency injection system makes FastAPI compatible with:
            all the relational databases
            NoSQL databases
            external packages
            external APIs
            authentication and authorization systems
            API usage monitoring systems
            response data injection systems
            etc.
    Simple and Powerful:
        Although the hierarchical dependency injection system is very simple to define and use, it's still very powerful.
        You can define dependencies that in turn can define dependencies themselves.
        In the end, a hierarchical tree of dependencies is built, and the Dependency Injection system takes care of solving all these dependencies for you (and their sub-dependencies) and providing (injecting) the results at each step.
        For example, let's say you have 4 API endpoints (path operations):
            /items/public/
            /items/private/
            /users/{user_id}/activate
            /items/pro/
        then you could add different permission requirements for each of them just with dependencies and sub-dependencies.
    Integrated with OpenAPI:
        All these dependencies, while declaring their requirements, also add parameters, validations, etc. to your path operations.
        FastAPI will take care of adding it all to the OpenAPI schema, so that it is shown in the interactive documentation systems

Classes as Dependencies:
    What makes a dependency:
        Up to now you have seen dependencies declared as functions.
        But that's not the only way to declare dependencies (although it would probably be the more common).
        The key factor is that a dependency should be a "callable".
        A "callable" in Python is anything that Python can "call" like a function.
        So, if you have an object something (that might not be a function) and you can "call" it (execute it) like:
            something()
            or
            something(some_argument, some_keyword_argument="foo")
        then it is a "callable".
        A Python class is a callable.
    Then, in FastAPI, you could use a Python class as a dependency.
    What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.
    If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable", and process them in the same way as the parameters for a path operation function. Including sub-dependencies.
    That also applies to callables with no parameters at all. The same as it would be for path operation functions with no parameters.
    Pay attention to the __init__ method used to create the instance of the class: ...it has the same parameters as our previous common_parameters.
    Those parameters are what FastAPI will use to "solve" the dependency. In both cases the data will be converted, validated, documented on the OpenAPI schema, etc.
    Now you can declare your dependency using this class.
    FastAPI calls the CommonQueryParams class. This creates an "instance" of that class and the instance will be passed as the parameter commons to your function.
    Type annotation vs Depends: (whatch the example).
    Shortcut:
        But you see that we are having some code repetition here, writing CommonQueryParams twice.
        FastAPI provides a shortcut for these cases, in where the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself.
        For those specific cases, you can do the following:
            commons: Annotated[CommonQueryParams, Depends()]
            You declare the dependency as the type of the parameter, and you use Depends() without any parameter, instead of having to write the full class again inside of Depends(CommonQueryParams).
        Tip: If that seems more confusing than helpful, disregard it, you don't need it. It is just a shortcut. Because FastAPI cares about helping you minimize code repetition.

Sub-dependencies:
    You can create dependencies that have sub-dependencies.
    They can be as deep as you need them to be.
    FastAPI will take care of solving them.
    Let's focus on the parameters declared: (Whatch the example)
        Even though this function is a dependency ("dependable") itself, it also declares another dependency (it "depends" on something else).
        It depends on the query_extractor, and assigns the value returned by it to the parameter q.
        It also declares an optional last_query cookie, as a str.
        If the user didn't provide any query q, we use the last query used, which we saved to a cookie before.
    Using the same dependency multiple times:
        If one of your dependencies is declared multiple times for the same path operation, for example, multiple dependencies have a common sub-dependency, FastAPI will know to call that sub-dependency only once per request.
        And it will save the returned value in a "cache" and pass it to all the "dependants" that need it in that specific request, instead of calling the dependency multiple times for the same request.
        In an advanced scenario where you know you need the dependency to be called at every step (possibly multiple times) in the same request instead of using the "cached" value, you can set the parameter use_cache=False when using Depends:
        async def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):
            return {"fresh_value": fresh_value}
    Recap:
        Apart from all the fancy words used here, the Dependency Injection system is quite simple.
        Just functions that look the same as the path operation functions.
        But still, it is very powerful, and allows you to declare arbitrarily deeply nested dependency "graphs" (trees).
        Tip: 
            All this might not seem as useful with these simple examples.
            But you will see how useful it is in the chapters about security.
            And you will also see the amounts of code it will save you.

Dependencies in path operation decorators:
    In some cases you don't really need the return value of a dependency inside your path operation function.
    Or the dependency doesn't return a value.
    But you still need it to be executed/solved.
    For those cases, instead of declaring a path operation function parameter with Depends, you can add a list of dependencies to the path operation decorator.
    Add dependencies to the path operation decorator:
        The path operation decorator receives an optional argument dependencies.
        It should be a list of Depends().
    These dependencies will be executed/solved the same way as normal dependencies. But their value (if they return any) won't be passed to your path operation function.
    Tip:
        Some editors check for unused function parameters, and show them as errors.
        Using these dependencies in the path operation decorator you can make sure they are executed while avoiding editor/tooling errors.
        It might also help avoid confusion for new developers that see an unused parameter in your code and could think it's unnecessary.
    Info:
        In this example we use invented custom headers X-Key and X-Token.
        But in real cases, when implementing security, you would get more benefits from using the integrated Security utilities (the next chapter).
    Dependencies errors and return values:
        You can use the same dependency functions you use normally.
        Dependency requirements:
            They can declare request requirements (like headers) or other sub-dependencies.
        Raise exceptions:
            These dependencies can raise exceptions, the same as normal dependencies.
        Return values:
            And they can return values or not, the values won't be used.
            So, you can reuse a normal dependency (that returns a value) you already use somewhere else, and even though the value won't be used, the dependency will be executed.
    Dependendecies for a group of path operations:
        Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.
    Global Dependencies:
        Next we will see how to add dependencies to the whole FastAPI application, so that they apply to each path operation.

Global Dependencies:
    For some types of applications you might want to add dependencies to the whole application.
    Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.
    In that case, they will be applied to all the path operations in the application.
    And all the ideas in the section about adding dependencies to the path operation decorators still apply, but in this case, to all of the path operations in the app.
    Dependencies for groups of path operations:
        Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.

Dependencies with yield:
    FastAPI supports dependencies that do some extra steps after finishing.
    To do this, use yield insted of return, and write the extra steps (code) after.
    Tip:
        Make sure to use yield one single time per dependency.
    Technical details:
        Any function that is valid to use with:
            @contextlib.contextmanager or
            @contextlib.asynccontextmanager
        would be valid to use as a FastAPI dependency.
        In fact, FastAPI uses those two decorators internally.
    A database dependency with yield:
        For example, you could use this to create a database session and close it after finishing.
        Only the code prior to and including the yield statement is executed before creating a response.
        The yielded value is what is injected into path operations and other dependencies.
        The code following the yield statement is executed after creating the response but before sending it.
        Tip:
            You can use async or regular functions.
            FastAPI will do the right thing with each, the same as with normal dependencies.
    A dependency with yield and try:
        If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependency.
        For example, if some code at some point in the middle, in another dependency or in a path operation, made a database transaction "rollback" or create any other error, you will receive the exception in your dependency.
        So, you can look for that specific exception inside the dependency with except SomeException.
        In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.
    Sub-dependencies with yield:
        You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use yield.
        FastAPI will make sure that the "exit code" in each dependency with yield is run in the correct order.
        The same way, you could have some dependencies with yield and some other dependencies with return, and have some of those depend on some of the others.
        And you could have a single dependency that requires several other dependencies with yield, etc.
        You can have any combinations of dependencies that you want.
        FastAPI will make sure everything is run in the correct order.
        Technical details:
            This works thanks to Python's Context Managers.
            FastAPI uses them internally to achive this.
    Dependencies with yield and HTTPException:
        You saw that you can use dependencies with yield and have try blocks that catch exceptions.
        The same way, you can raise an HTTPException or similar in the exit code, after the yield.
        Tip:
            This is a somewhat advanced technique, and in most of the cases you won't really need it, as you can raise exceptions (including HTTPException) from inside of the rest of your application code, for example, in the path operation function.
            But it's there for you if you need it. 
        An alternative you could use to catch exceptions (and possibly also raise another HTTPException) is to create a Custom Exception Handler.
    Dependencies with yield and exept:
        If you catch an exception using except in a dependency with yield and you don't raise it again (or raise a new exception), FastAPI won't be able to notice there was an exception, the same way that would happen with regular Python.
        In this case, the client will see an HTTP 500 Internal Server Error response as it should, given that we are not raising an HTTPException or similar, but the server will not have any logs or any other indication of what was the error. 
    Always raise in Dependencies with yield and except:
        If you catch an exception in a dependency with yield, unless you are raising another HTTPException or similar, you should re-raise the original exception.
    Execution of dependencies with yield:
        The sequence of execution is more or less like this diagram. Time flows from top to bottom. And each column is one of the parts interacting or executing code. (See diagram).
        Info:
            Only one response will be sent to the client. It might be one of the error responses or it will be the response from the path operation.
            After one of those responses is sent, no other response can be sent.
        Tip:
            This diagram shows HTTPException, but you could also raise any other exception that you catch in a dependency with yield or with a Custom Exception Handler.
            If you raise any exception, it will be passed to the dependencies with yield, including HTTPException. In most cases you will want to re-raise that same exception or a new one from the dependency with yield to make sure it's properly handled.
    Dependencies with yield, HTTPException, except and Background Tasks:
        Warning:
            You most probably don't need these technical details, you can skip this section and continue below.
            These details are useful mainly if you were using a version of FastAPI prior to 0.106.0 and used resources from dependencies with yield in background tasks.
    Context Managers:
        "Context Managers" are any of those Python objects that you can use in a with statement.
        For example, you can use with to read a file:
            with open("./somefile.txt") as f:
                contents = f.read()
                print(contents)
        Underneath, the open("./somefile.txt") creates an object that is called a "Context Manager".
        When the with block finishes, it makes sure to close the file, even if there were exceptions.
        When you create a dependency with yield, FastAPI will internally create a context manager for it, and combine it with some other related tools.
    Using context manager in dependencies with yield:
        Warning:
            This is, more or less, an "advanced" idea.
            If you are just starting with FastAPI you might want to skip it for now.
        In Python, you can create Context Managers by creating a class with two methods: __enter__() and __exit__().
        You can also use them inside of FastAPI dependencies with yield by using with or async with statements inside of the dependency function.
        Tip:
            Another way to create a context manager is with:
                @contextlib.contextmanager or
                @contextlib.asynccontextmanager
            using them to decorate a function with a single yield.
            That's what FastAPI uses internally for dependencies with yield.
            But you don't have to use the decorators for FastAPI dependencies (and you shouldn't).
            FastAPI will do it for you internally.

Security:
    There are many ways to handle security, authentication and authorization.
    And it normally is a complex and "difficult" topic.
    In many frameworks and systems just handling security and authentication takes a big amount of effort and code (in many cases it can be 50% or more of all the code written).
    FastAPI provides several tools to help you deal with Security easily, rapidly, in a standard way, without having to study and learn all the security specifications.
    But first, let's check some small concepts.
    OAuth2:
        OAuth2 is a specification that defines several ways to handle authentication and authorization.
        It is quite an extensive specification and covers several complex use cases.
        It includes ways to authenticate using a "third party".
        That's what all the systems with "login with Facebook, Google, Twitter, GitHub" use underneath.
    OAuth 1:
        There was an OAuth 1, which is very different from OAuth2, and more complex, as it included direct specifications on how to encrypt the communication.
        It is not very popular or used nowadays.
        OAuth2 doesn't specify how to encrypt the communication, it expects you to have your application served with HTTPS.
        Tip:
            In the section about deployment you will see how to set up HTTPS for free, using Traefik and Let's Encrypt.
    OpenID Connect:
        OpenID Connect is another specification, based on OAuth2.
        It just extends OAuth2 specifying some things that are relatively ambiguous in OAuth2, to try to make it more interoperable.
        For example, Google login uses OpenID Connect (which underneath uses OAuth2).
        But Facebook login doesn't support OpenID Connect. It has its own flavor of OAuth2.
    OpenID (not "OpenID Connect"):
        There was also an "OpenID" specification. That tried to solve the same thing as OpenID Connect, but was not based on OAuth2.
        So, it was a complete additional system.
        It is not very popular or used nowadays.
    OpenAPI:
        OpenAPI (previously known as Swagger) is the open specification for building APIs (now part of the Linux Foundation).
        FastAPI is based on OpenAPI.
        That's what makes it possible to have multiple automatic interactive documentation interfaces, code generation, etc.
        OpenAPI has a way to define multiple security "schemes".
        By using them, you can take advantage of all these standard-based tools, including these interactive documentation systems.
        OpenAPI defines the following security schemes:
            apiKey: an application specific key that can come from:
                A query parameter.
                A header.
                A cookie.
            http: standard HTTP authentication systems, including:
                bearer: a header Authorization with a value of Bearer plus a token. This is inherited from OAuth2.
                HTTP Basic authentication.
                HTTP Digest, etc.
            oauth2: all the OAuth2 ways to handle security (called "flows").
                Several of these flows are appropriate for building an OAuth 2.0 authentication provider (like Google, Facebook, Twitter, GitHub, etc):
                    implicit
                    clientCredentials
                    authorizationCode
                But there is one specific "flow" that can be perfectly used for handling authentication in the same application directly:
                    password: some next chapters will cover examples of this.
                    openIdConnect: has a way to define how to discover OAuth2 authentication data automatically.
                This automatic discovery is what is defined in the OpenID Connect specification.
    Tip:
        Integrating other authentication/authorization providers like Google, Facebook, Twitter, GitHub, etc. is also possible and relatively easy.
        The most complex problem is building an authentication/authorization provider like those, but FastAPI gives you the tools to do it easily, while doing the heavy lifting for you.
    FastAPI utilities:
        FastAPI provides several tools for each of these security schemes in the fastapi.security module that simplify using these security mechanisms.
        In the next chapters you will see how to add security to your API using those tools provided by FastAPI.
        And you will also see how it gets automatically integrated into the interactive documentation system.

Security - First Steps:
    Let's imagine that you have your backend API in some domain.
    And you have a frontend in another domain or in a different path of the same domain (or in a mobile application).
    And you want to have a way for the frontend to authenticate with the backend, using a username and password.
    We can use OAuth2 to build that with FastAPI.
    But let's save you the time of reading the full long specification just to find those little pieces of information you need.
    Let's use the tools provided by FastAPI to handle security.
    Info:
        The python-multipart package is automatically installed with FastAPI when you run the pip install "fastapi[standard]" command.
        However, if you use the pip install fastapi command, the python-multipart package is not included by default.
        To install it manually, make sure you create a virtual environment, activate it, and then install it with:
            pip install python-multipart
        This is because OAuth2 uses "form data" for sending the username and password.
    Authorize button:
        You already have a shiny new "Authorize" button.
        And your path operation has a little lock in the top-right corner that you can click.
        And if you click it, you have a little authorization form to type a username and password (and other optional fields).
    This is of course not the frontend for the final users, but it's a great automatic tool to document interactively all your API.
    It can be used by the frontend team (that can also be yourself).
    It can be used by third party applications and systems.
    And it can also be used by yourself, to debug, check and test the same application.
    The password flow:
        Now let's go back a bit and understand what is all that.
        The password "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.
        OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.
        But in this case, the same FastAPI application will handle the API and the authentication.
        So, let's review it from that simplified point of view:
            The user types the username and password in the frontend, and hits Enter.
            The frontend (running in the user's browser) sends that username and password to a specific URL in our API (declared with tokenUrl="token").
            The API checks that username and password, and responds with a "token" (we haven't implemented any of this yet).
                A "token" is just a string with some content that we can use later to verify this user.
                Normally, a token is set to expire after some time.
                    So, the user will have to log in again at some point later.
                    And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).
            The frontend stores that token temporarily somewhere.
            The user clicks in the frontend to go to another section of the frontend web app.
            The frontend needs to fetch some more data from the API.
                But it needs authentication for that specific endpoint.
                So, to authenticate with our API, it sends a header Authorization with a value of Bearer plus the token.
                If the token contains foobar, the content of the Authorization header would be: Bearer foobar.
    FastAPI's OAuth2PasswordBearer:
        FastAPI provides several tools, at different levels of abstraction, to implement these security features.
        In this example we are going to use OAuth2, with the Password flow, using a Bearer token. We do that using the OAuth2PasswordBearer class.
        Info:
            A "bearer" token is not the only option.
            But it's the best one for our use case.
            And it might be the best for most use cases, unless you are an OAuth2 expert and know exactly why there's another option that better suits your needs.
            In that case, FastAPI also provides you with the tools to build it.
        When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.
        This parameter doesn't create that endpoint / path operation, but declares that the URL /token will be the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.
        We will soon also create the actual path operation.
    What it does:
        It will go and look in the request for that Authorization header, check if the value is Bearer plus some token, and will return the token as a str.
        If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (UNAUTHORIZED) directly.
        You don't even have to check if the token exists to return an error. You can be sure that if your function is executed, it will have a str in that token.
        You can try it already in the interactive docs.
        We are not verifying the validity of the token yet, but that's a start already.
    Recap:
        So, in 3 or 4 extra lines, you already have some primitive form of security.

Get Current User:
    In the previous chapter the security system (which is based on the dependency injection system) was giving the path operation function a token as a str. But that is still not that usefull. Let's make it give us the current user.
    Create a user model:
        First, let's create a Pydantic user model.
        The same way we use Pydantic to declare bodies, we can use it anywhere else.
    Create get_current_user dependency:
        Remember that dependencies can have sub-dependencies?
        get_current_user will have a dependency with the same oauth2_scheme we created before.
        The same as we were doing before in the path operation directly, our new dependency get_current_user will receive a token as a str from the sub-dependency oauth2_scheme
    Get the user:
        get_current_user will use a (fake) utility function we created, that takes a token as a str and returns our Pydantic User model.
    Inject the current user:
        So now we can use the same Depends with our get_current_user in the path operation.
    Notice that we declare the type of current_user as the Pydantic model User.
    This will help us inside of the function with all the completion and type checks
    Tip:
        You might remember that request bodies are also declared with Pydantic models.
        Here FastAPI won't get confused because you are using Depends.
    Check:
        The way this dependency system is designed allows us to have different dependencies (different "dependables") that all return a User model.
        We are not restricted to having only one dependency that can return that type of data.
    Other models:
        You can now get the current user directly in the path operation functions and deal with the security mechanisms at the Dependency Injection level, using Depends.
        And you can use any model or data for the security requirements (in this case, a Pydantic model User).
        But you are not restricted to using some specific data model, class or type.
        Do you want to have an id and email and not have any username in your model? Sure. You can use these same tools.
        Do you want to just have a str? Or just a dict? Or a database class model instance directly? It all works the same way.
        You actually don't have users that log in to your application but robots, bots, or other systems, that have just an access token? Again, it all works the same.
        Just use any kind of model, any kind of class, any kind of database that you need for your application. FastAPI has you covered with the dependency injection system.
    Code size:
        This example might seem verbose. Keep in mind that we are mixing security, data models, utility functions and path operations in the same file.
        But here's the key point.
        The security and dependency injection stuff is written once.
        And you can make it as complex as you want. And still, have it written only once, in a single place. With all the flexibility.
        But you can have thousands of endpoints (path operations) using the same security system.
        And all of them (or any portion of them that you want) can take advantage of re-using these dependencies or any other dependencies you create.
        And all these thousands of path operations can be as small as 3 lines.
    Recap:
        You can now get the current user directly in your path operation function.
        We are already halfway there.
        We just need to add a path operation for the user/client to actually send the username and password.
        That comes next.






Middleware:
CORS (Cross-Origin Resource Sharing):
SQL (Relational) Databases:
Bigger Aplications - Multiple Files:
Background Tasks:
Metadata and Docs URLs:
Static Files:
Testing:
Debugging: