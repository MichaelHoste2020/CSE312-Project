from fastapi import *

class ConnectionManager:
    def __init__(self):
        self.sockets: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        id = str(websocket.client.host) + ":" + str(websocket.client.port)
        self.sockets[id] = websocket

    async def disconnect(self, id: str):
        print("before", self.sockets)
        self.sockets.pop(id)
        print("after", self.sockets)       

    # send message to a single websocket
    async def sendDirectMessage(self, message, websocket: WebSocket):
        await websocket.send_text(message)

    # sends a message to every socket except current
    async def broadcast(self, message, current: WebSocket):
        for socket in self.sockets.values():
            if socket != current:
                await socket.send_text(message)