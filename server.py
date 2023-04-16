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

@app.get("/signup.html")
async def start():
    return FileResponse("src/html/signup.html")

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

# Handles user login/signup
@app.post("/data")
async def storeUser(username: str = Form (...), password: str = Form (...)):
    userdb.storeUser(username, password)
    return RedirectResponse("", status.HTTP_204_NO_CONTENT)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)