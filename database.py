from pymongo import MongoClient
import html
import bcrypt
import secrets
import json

class db():

    # mongo_Client = MongoClient(
    #     "mongodb+srv://mike:NqCsSQC8E8Arjcwd@cluster0.pkpo8iw.mongodb.net/?retryWrites=true&w=majority")
    mongo_Client = MongoClient("mongo")
    db = mongo_Client["database"]
    userCollection = db["users"]

    # mongoClient = MongoClient("mongo")
    # database = mongoClient["database"]
    # userCollection = database["users"]
    
    def storeUser(self, username, password):

        # Make sure that the user is logging in correctly
        for user in self.userCollection.find({}):
            if user == username:
                return False

        # Check for html injection
        username = html.escape(username)
        password = html.escape(password)
        password = password.encode('utf-8')

        # Salt the password || encrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        token = secrets.token_urlsafe(20)

        self.userCollection.insert_one(
            {"username": username, "password": hashed_password.decode(), "salt": salt.decode(), "score": 0, "auth": token})

        return True

        
    def getUsers(self):
        users = []
        
        for user in self.userCollection.find({}):
            user.pop("_id")
            users.append(user)
            
        return users

    def auth_User(self, username, password):

        for user in self.userCollection.find({}):
            print(user)
            hashed_password = bcrypt.hashpw(password.encode(
                "utf-8"), user.get('salt').encode("utf-8"))
            if user.get("username") == username:
                if user.get("password") == hashed_password.decode():
                    print("User is now logged in and passing back auth token ")
                    return user["auth"]

        return ""
