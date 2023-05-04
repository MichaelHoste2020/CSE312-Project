import uvicorn
import json
from database import db
from fastapi import *
from fastapi.staticfiles import StaticFiles
from starlette.responses import *  # fastAPI is based off starlette
from fastapi.templating import Jinja2Templates
import bcrypt
from functions import *

app = FastAPI()
userdb = db()

# IMPORTANT: DELETE THIS, ONLY FOR DEMOING

templates = Jinja2Templates(directory="src/html")


@app.get("/users")
async def getUsers():
    return userdb.getUsers()


@app.post("/logout")
async def getUsers(request: Request, response: Response):
    response.delete_cookie(key="auth")
    return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)


@app.get("/")
async def login_signup(request: Request, response: Response):
    # grabbing the value of "visits" cookie from response headers
    visitsCookie = request.cookies.get("visits")
    # response starts off as FileResponse and then add a cookie on top of that with set_cookie
    response = FileResponse("src/html/index.html")

    if visitsCookie:
        response.set_cookie(key="visits", value=int(visitsCookie)+1)
    else:
        response.set_cookie(key="visits", value=1)
    return response


@app.get("/home")
async def homePage(request: Request):

    auth = request.cookies.get("auth_token")
    print("This is the current auth token {0}".format(auth))

    # If we are not authenticated return to main page
    if auth == None:
        return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)
    elif (userdb.Auth_Cookie_Check(auth) == False):
        return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)

    name = userdb.Current_User(auth)

    users = []

    for user in userdb.userCollection.find({}):
        users.append({"username": user["username"], "score": user["score"]})

    return templates.TemplateResponse("home.html", {"request": request, "username": name, "users": users})


@app.get("/styles/home.css")
async def start():
    print("getting new css")
    return FileResponse("src/styles/home.css")


@app.get("/signup")
async def start():
    return FileResponse("src/html/index.html")


@app.get("/styles/main.css")
async def start():
    return FileResponse("src/styles/main.css")


@app.get("/styles/signup.css")
async def start():
    return FileResponse("src/styles/signup.css")


@app.get("/images/logo.svg")
async def getLogo():
    return FileResponse("src/images/logo.svg")


@app.get("/js/main.js")
async def script():
    return FileResponse("src/js/main.js")

# Handles user login


@app.post("/login")
async def getuser(username: str = Form(...), password: str = Form(...)):

    # Check and see if they are already logged in
    return_Info = userdb.auth_User(username, password)

    # bad request here
    if return_Info == "":
        print("bad")
        return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)
    response = RedirectResponse("/home", status.HTTP_301_MOVED_PERMANENTLY)
    response.set_cookie(key="auth_token", value=return_Info)
    return response

# Handles Signup


@app.post("/signup")
async def storeUser(username: str = Form(...), password: str = Form(...)):
    return_Type = userdb.storeUser(username, password)

    # This is to make sure that a new user does not have the same name
    if return_Type == True:
        return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)
    return RedirectResponse("", status.HTTP_401_UNAUTHORIZED)


@app.post("/change-account")
async def change_Account_Info(request: Request,username: str = Form(...), password: str = Form(...)):
    
    cookie = request.cookies.get("auth_token")
    
    return_Type = userdb.Change_User_Info(username, password,cookie)

    # This is to make sure that a new user does not have the same name
    if return_Type == True:
        return RedirectResponse("/home", status.HTTP_301_MOVED_PERMANENTLY)
    return RedirectResponse("/", status.HTTP_401_UNAUTHORIZED)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
