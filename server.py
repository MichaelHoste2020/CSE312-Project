import uvicorn
import json
from database import db
from fastapi import *
from fastapi.staticfiles import StaticFiles
from starlette.responses import * #fastAPI is based off starlette
from fastapi.templating import Jinja2Templates
from Classes import *
import bcrypt

app = FastAPI()
userdb = db()
manager = ConnectionManager()
clients = {}
sockets = {}

# IMPORTANT: DELETE THIS, ONLY FOR DEMOING
@app.get("/users")
async def getUsers():
    return userdb.getUsers()

@app.get("/")
async def start(request: Request, response: Response):
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
async def start():
    name = find_Current_User()
    return Jinja2Templates.TemplateResponse("src/html/home.html",{"username": name})

@app.get("/signup")
async def start():
    return FileResponse("src/html/index.html")

@app.get("/game")
async def game():
    return FileResponse("src/html/game.html")

@app.get("/js/{filename}.js")
async def script(filename: str):
    return FileResponse(f"src/js/{filename}.js")

@app.get("/styles/{filename}.css")
async def start(filename: str):
    return FileResponse(f"src/styles/{filename}.css")

@app.get("/images/logo.svg")
async def getLogo():
    return FileResponse("src/images/logo.svg")

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

# Websocket connection for lobby
@app.websocket("/lobby")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        id = str(websocket.client.host) + ":" + str(websocket.client.port)
        while True:
            data = await websocket.receive()
            print(data)
            type = data.get("type")
            
            if data.get("text"):
                if json.loads(data.get("text")):
                    textType = json.loads(data.get("text")).get("type")
                    if textType == "new_user":
                        message = json.dumps({"client": id, "x": 0, "y": 0, "infoType": "new_user"})
                        await manager.sendDirectMessage(message, websocket)
                    else:
                        location = json.loads(data.get("text"))
                        location["id"] = id
                        location["infoType"] = "location"
                        message = json.dumps(location)
                        await manager.broadcast(message, websocket)
            elif type == "websocket.disconnect":
                raise WebSocketDisconnect
    except WebSocketDisconnect:
        await manager.disconnect(id)
        print(f"{websocket.client} has disconnected")
    
def auth_check(DataBase_Users, Incoming_Auth_Token):

    for user in DataBase_Users:
        if user["auth"] == Incoming_Auth_Token:
            return True
    return False

def find_Current_User(userdb,auth_Token):
    for user in userdb:
        check = bcrypt.hashpw(auth_Token,user["salt"])
        if user["auth_Token"] == check:
            return user["username"]
        
    return ""

def list_User(user_db):

    user_List = []

    for user in user_db.find({}):
        user_List.append({"username":user["username"],"Score":user["score"]})
    return user_List

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)