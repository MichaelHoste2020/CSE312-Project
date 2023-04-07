from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse #fastAPI is based off starlette
from pymongo import MongoClient

app = FastAPI()

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

@app.get("/websocket.js")
async def script():
    return FileResponse("src/js/websocket.js")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")