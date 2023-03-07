**DOC:** `https://fastapi.tiangolo.com/tutorial/first-steps/`

**REPO:** `https://github.com/tiangolo/fastapi`

* License: MIT License

  * Description:

    * Anyone can obtain a free copy of FastAPI so long as it deals with software use. They can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software

  * Restrictions:

    * No warranty and/or liability. Copyright owners are not held responsible for any claim, damages, or other liabilities that may arise.


**\* Install**

  ```
  pip install fastapi
  pip install "uvicorn[standard]"
  ```

  * `uvicorn`

    * A ASGI web server implementation

    * Acts as our server to host code

    * Allows for async frameworks for python

**\* Hello world**

  ```py
  from fastapi import FastAPI
  
  app = FastAPI()
  
  @app.get("/")
  async def root():
      return {"message": "Hello World"}
  
  @app.get("/redirect")
  async def redirect():
    return {"message": "Redirected"}
  ```

  * `FastAPI()`

    * Location

      * master/fastapi/application.py

      * Line: 48

    * Class call that provides us access to all functions within FastAPI

  * `@app.get("/")`

    * Location

      * master/fastapi/application.py

      * Line: 438

    * `.get()` has multiple arguments, but the required one is the path, in the example its path `/`

    * When `.get()` is invoked, it takes the arguments and passes them into another `.get()`function located in master/fastapi/router.py on line 833. This new `.get()`function passes these arguments to the `api_route` function located in the same file on line 629. `api_route` then adds the new route by passing the arguments to the function `add_api_route` on line 547. This function is what builds the routing and appends it to a list of routes called `routes`. When the server starts it will check for whenever a route is called and reference the defined function declared below each respected `.get()`. In this example, when a client requests `/`, the function `root()` will be called.

  * `@app.get("/redirect")`
    
    * Will trigger when user makes a url request to `/redirect`

    * You can test this by adding changing your url to `http://127.0.0.1:8000/redirect`

**\* Running The Server**

  ```py
  uvicorn server:app --reload
  ```

  * `server` refers to the file name, in our example the python file is called `server.py`

  * `app` refers to the variable set to `FastAPI()` in our example it’ll be `app = FastAPI()`

  * `--reload` does a server restart for code change, only use for development

**\* Interactive API docs**
  `http://127.0.0.1:8000/docs`
  * FastAPI has their own interactive API doc that is tied with the server you're Running
  
  * This page will show all requests, outlining the responses, description, etc.
