from pymongo import MongoClient
import html
import bcrypt
import secrets
import json

class db():

    mongo_Client = MongoClient(
        "mongodb+srv://mike:NqCsSQC8E8Arjcwd@cluster0.pkpo8iw.mongodb.net/?retryWrites=true&w=majority")
    # mongo_Client = MongoClient("mongo")
    db = mongo_Client["database"]
    userCollection = db["users"]

    # mongoClient = MongoClient("mongo")
    # database = mongoClient["database"]
    # userCollection = database["users"]
    
    def storeUser(self, username, password):

        # Make sure that the user is logging in correctly
        print(self.userCollection.find({}))
        for user in self.userCollection.find({}):
            if user == username:
                return False

        # Check for html injection
        username = html.escape(username)
        password = html.escape(password)
        password = password.encode('utf-8')

        print("start salt")
        # Salt the password || encrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        token = secrets.token_urlsafe(20)
        print("This is the type of the token {0}".format(type(token)))
        token_Safe = bcrypt.hashpw(token.encode("utf-8"), salt)

        print("storing")
        self.userCollection.insert_one({"username": username, "password": hashed_password, "salt": salt, "score": 0, "auth": token_Safe})

        print("done")
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
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), user.get('salt'))
            if user.get("username") == username:
                if user.get("password") == hashed_password:
                    print("User is now logged in and passing back auth token ")

                    token = secrets.token_urlsafe(20)
                    storage = bcrypt.hashpw(
                        token.encode("utf-8"), user.get("salt"))
                    self.userCollection.update_one({"username": username}, {
                        '$set': {"auth": storage}})
                    return token

        return ""

    def Auth_Cookie_Check(self, token):

        for user in self.userCollection.find({}):
            hashed_auth = bcrypt.hashpw(
                token.encode("utf-8"), user.get("salt"))
            if user.get("auth") == hashed_auth:
                return True
        return False

    def Current_User(self, token):

        for user in self.userCollection.find({}):
            hashed_auth = bcrypt.hashpw(
                token.encode("utf-8"), user.get("salt"))
            if user.get("auth") == hashed_auth:
                return user.get("username")
        return ""

    def Change_User_Info(self, username, password, token):

        # no duplicate users
        for user in self.userCollection.find({}):
            if user == username:
                return False

        # Check for html injection
        username = html.escape(username)
        password = html.escape(password)

        for user in self.userCollection.find({}):
            hashed_auth = bcrypt.hashpw(
                token.encode("utf-8"), user.get("salt"))
            if user.get("auth") == hashed_auth:

                if password != "":
                    password = password.encode('utf-8')
                    hashed_password = bcrypt.hashpw(password, user["salt"])
                    self.userCollection.update_one({"username": user["username"]}, {
                        '$set': {"password": hashed_password}})

                if username != "":
                    self.userCollection.update_one({"username": user["username"]}, {
                        '$set': {"username": username}})

                return True
        return False
