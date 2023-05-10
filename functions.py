import bcrypt

def auth_check(DataBase_Users, Incoming_Auth_Token):
    
    for user in DataBase_Users:
        token = bcrypt.hashpw(Incoming_Auth_Token,user["salt"])
        if user["auth"] == token:
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