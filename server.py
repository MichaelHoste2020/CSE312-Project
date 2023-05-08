import uvicorn
import json
from database import db
from fastapi import *
from fastapi.staticfiles import StaticFiles
from starlette.responses import *  # fastAPI is based off starlette
from fastapi.templating import Jinja2Templates
from Classes import *
import bcrypt
from functions import *

app = FastAPI()
userdb = db()
manager = ConnectionManager()
clients = {}
sockets = {}
templates = Jinja2Templates(directory="src/html")

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

@app.get("/game")
async def game(request: Request, response_class=HTMLResponse):
    name = request.cookies.get("name")
    
    if name:
        return templates.TemplateResponse("game.html", {"request": request, "name": name})
    
    return PlainTextResponse("No user logged in", status_code=404)

@app.get("/js/{filename}.js")
async def script(filename: str):
    return FileResponse(f"src/js/{filename}.js")

@app.get("/styles/{filename}.css")
async def start(filename: str):
    return FileResponse(f"src/styles/{filename}.css")


@app.get("/images/logo.svg")
async def getLogo():
    return FileResponse("src/images/logo.svg")

@app.get("/images/goose.ico")
async def getGoose():
    return FileResponse("src/images/goose.ico")

# Handles user login

@app.post("/login")
async def getuser(username: str = Form(...), password: str = Form(...)):

    # Check and see if they are already logged in
    return_Info = userdb.auth_User(username, password)

    # bad request here
    if return_Info == "":
        print("bad")
        # otherwise it sets the return_Info as a cookie of authorication which Will be checked
        return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)
    response = RedirectResponse("/game", status.HTTP_301_MOVED_PERMANENTLY)
    response.set_cookie(key="name", value=username)
    response.set_cookie(key="auth_token", value=return_Info)
    return response

# Handles Signup


@app.post("/signup")
async def storeUser(username: str = Form(...), password: str = Form(...)):
    return_Type = userdb.storeUser(username, password)
    
    # This is to make sure that a new user does not have the same name
    if return_Type == True:
       return RedirectResponse("/", status.HTTP_301_MOVED_PERMANENTLY)
    return RedirectResponse("/", status.HTTP_401_UNAUTHORIZED)


@app.post("/change-account")
async def change_Account_Info(request: Request,username: str = Form(...), password: str = Form(...)):
    
    cookie = request.cookies.get("auth_token")
    
    return_Type = userdb.Change_User_Info(username, password,cookie)

    # This is to make sure that a new user does not have the same name
    if return_Type == True:
        return RedirectResponse("/home", status.HTTP_301_MOVED_PERMANENTLY)
    return RedirectResponse("/", status.HTTP_401_UNAUTHORIZED)


# Websocket connection for lobby
lobbies = {}
lobbyID = 0
@app.websocket("/lobby")
async def websocket_endpoint(websocket: WebSocket):
    try:
        global lobbies
        global lobbyID
        await manager.connect(websocket)
        id = str(websocket.client.host) + ":" + str(websocket.client.port)
        while True:
            data = await websocket.receive()
            #print(data)
            #print(clients)
            type = data.get("type")
            
            if data.get("text"):
                if json.loads(data.get("text")):
                    textType = json.loads(data.get("text")).get("type")
                    #print(textType)
                    
                    # when someone wins send a "winner" response to winner and "loser" response to everyone else
                    if textType == "winner":
                        print("winner")
                        winnerMsg = json.dumps({ "infoType": "winner"})
                        LoserMsg = json.dumps({ "infoType": "loser" })
                        await manager.sendDirectMessage(winnerMsg, websocket)
                        #FIXME: change this so it only sends to the other client, broadcasting sends it to everyone
                        await manager.broadcast(LoserMsg, websocket)

                    if textType == "new_user":
                        # if the current lobby is maxed out, go to the next avaliable one
                        print( len(lobbies.get(lobbyID, [])) )
                        if len(lobbies.get(lobbyID, [])) >= 2: 
                            print("making new lobby")
                            lobbyID += 1
                        
                        # when new user detected add client to data structure
                        clients[id] = {"lobbyID": lobbyID, "x": 0, "y": 0}
                        # add client to existing lobby else create new one if previous was full/non-existant
                        if lobbies.get(lobbyID):
                            lobbies.get(lobbyID).append(id)
                        else:
                            lobbies[lobbyID] = [id]
                        
                        message = json.dumps({"client": id, "x": 0, "y": 0, "infoType": "new_user"})
                        await manager.sendDirectMessage(message, websocket)
                        print(id, clients[id])
                        print(lobbies, "lobbyID:", lobbyID)
                    else:
                        # get location data
                        location = json.loads(data.get("text"))
                        location["client"] = id
                        location["infoType"] = "location"
                        
                        # update location data on server side for client
                        clients[id]["x"] = location.get("x")
                        clients[id]["y"] = location.get("y")
                        
                        # get the other client in the same lobby if one exists
                        otherClient = None
                        currentLobbyID = clients.get(id).get("lobbyID", -1)
                        if currentLobbyID != -1:
                            if len(lobbies.get(currentLobbyID, [])) >= 2:
                                if lobbies.get(currentLobbyID)[0] != id:
                                    otherClient = lobbies.get(currentLobbyID)[0]
                                else:
                                    otherClient = lobbies.get(currentLobbyID)[1]
                            
                            # if there is another client in lobby, send the clients location data to them
                            if otherClient:
                                otherSocket = manager.getSocket(otherClient)

                                message = json.dumps(location)
                                #print("---------\nLobby:", lobbies.get(currentLobbyID), "\nClient:", id, "\nOther client:", otherClient, "\nMessage:", message,"\n--------")
                                await manager.sendDirectMessage(message, otherSocket)
            elif type == "websocket.disconnect":
                raise WebSocketDisconnect
    except WebSocketDisconnect:
        inLobby = clients.get(id).get("lobbyID")
        
        lobby = lobbies.get(inLobby, [])
        
        # tell the other player their opponent left
        if len(lobby) >= 2:
            otherClient = None
            if (lobby[0] != id):
                otherClient = lobby[0]
            else:
                otherClient = lobby[1]
            
            if otherClient:
                otherSocket = manager.getSocket(otherClient)
                message = json.dumps({"infoType": "opponent_left"})
                await manager.sendDirectMessage(message, otherSocket)
            
        await manager.disconnect(id)
        clients.pop(id)
        lobbyID+=1
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