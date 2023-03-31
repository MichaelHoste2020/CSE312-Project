from pymongo import MongoClient
import socketserver
from Network import *


# This will be used to connect to mongoDB which will be used for this assignment
mongo_Client = MongoClient(
    "mongodb+srv://mike:NqCsSQC8E8Arjcwd@cluster0.pkpo8iw.mongodb.net/?retryWrites=true&w=majority")
# mongo_Client = MongoClient("mongo")
db = mongo_Client["cse312"]
logs_collection = db["logs"]

# Class structure to handle connections


class MyTCPHandler(socketserver.BaseRequestHandler):

    Socket_Collection = []

    def handle(self):

        recieved_data = self.request.recv(2048)

        # Incoming packet
        print(recieved_data)

        if recieved_data.find(b"websocket", 0, 20) != 0:

            self.Socket_Collection.append("id": self.client_address, "socket": self)

        # This in case we have no more information
        if len(recieved_data) == 0:
            return

        Network_Router(self, logs_collection, recieved_data)


# This is will be used for some local behavior but the below will have to change for production
if __name__ == "__main__":
    host = "0.0.0.0"  # This will have to change for production
    port = 8000

    # Threading will allow for more people in the server
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
