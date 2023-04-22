
def Network_Router(socket, account_collection, message):
    paths = ["/", "/main.css"]

    if message["req_method"] == "GET":
        for x in paths:
            if x == message["req_uri"]:
                Send_Message(socket, x)
    if message["req_method"] == "POST":
        if message["req_uri"] == "/login":
            Post_Login(socket, message)

    if message["req_method"] == "DELETE":
        print("get")
    if message["req_method"] == "PUT":
        print("get")


def Send_Message(socket, path):

    # This will be the GET methods
    if path == "/":
        print("pass the html")
        file = open("index.html", "r")
        msg = file.read()
        socket.request.sendall(
            "HTTP/1.1 200 Ok \r\nContent-Length: {0}\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff \r\n\r\n{1}".format(len(msg), msg).encode())
    if path == "/main.css":
        print("Pass the CSS")
        file = open("main.css", "r")
        msg = file.read()
        socket.request.sendall(
            "HTTP/1.1 200 Ok \r\nContent-Length: {0}\r\nContent-Type: text/css; charset=utf-8\r\nX-Content-Type-Options: nosniff \r\n\r\n{1}".format(len(msg), msg).encode())


def Post_Login(socket, message, account_collection):
    print()
