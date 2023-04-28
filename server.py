import uvicorn
import json
from database import db
from fastapi import *
from fastapi.staticfiles import StaticFiles
from starlette.responses import * #fastAPI is based off starlette

app = FastAPI()
userdb = db()

# IMPORTANT: DELETE THIS, ONLY FOR DEMOING
@app.get("/users")
async def getUsers():
    return userdb.getUsers()

@app.get("/")
async def start():
    return FileResponse("src/html/index.html")

@app.get("/home")
async def start():
    return FileResponse("src/html/home.html")

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

    return_Info = userdb.auth_User(username, password)

    if return_Info == "":
        # bad request here
        print("bad")
        # otherwise it sets the return_Info as a cookie of authorication which Will be checked
    return RedirectResponse("/home", status.HTTP_301_MOVED_PERMANENTLY)

# Handles Signup


@app.post("/signup")
async def storeUser(username: str = Form(...), password: str = Form(...)):
    return_Type = userdb.storeUser(username, password)

    # This is to make sure that a new user does not have the same name
    if return_Type == True:
        return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)
    return RedirectResponse("", status.HTTP_401_UNAUTHORIZED)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)


def auth_check(DataBase_Users, Incoming_Auth_Token):

    for user in DataBase_Users:
        if user["auth"] == Incoming_Auth_Token:
            return True
    return False
