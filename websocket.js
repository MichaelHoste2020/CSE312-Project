//Creating websocket url (where websocket will listen):
//  start the url with 'ws', special protocal to init a websocket
//  follow with target url, our case localhost at port 8080
//  end with /ws
var ws = new WebSocket("ws://localhost:8000/ws");

// onmessage triggered everytime websocket recieves data
ws.onmessage = function(event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};

function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}