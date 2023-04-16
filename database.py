from pymongo import MongoClient

class db():
    mongoClient = MongoClient("mongo")
    database = mongoClient["database"]
    userCollection = database["users"]
    
    # IMPORTANT: ENCRYPT THE PASSWORD, 
    # THIS IS CURRENTLY ONLY A PROOF OF CONCEPT FOR STORING USERS
    def storeUser(self, username, password):
        self.userCollection.insert_one({"username": username, "password": password})
        
    def getUsers(self):
        users = []
        
        for user in self.userCollection.find({}):
            user.pop("_id")
            users.append(user)
            
        return users