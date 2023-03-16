from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse #fastAPI is based off starlette

app = FastAPI()

@app.get("/")
async def start():
    return FileResponse("index.html")

@app.get("/websocket.js")
async def script():
    return FileResponse("websocket.js")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")