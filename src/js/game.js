var ws = new WebSocket('wss://' + window.location.host + '/ws');
var gameScene = null;
var clients = {};

var config = {
    type: Phaser.CANVAS,
    scale: {
        mode: Phaser.Scale.FIT,
        parent: 'game-container',
        width: 40,
        height: 800
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

var game = new Phaser.Game(config);
var grid = null;
var players = {};
var currentPlayer;
var opponentConnected = true;


function preload ()
{
}

function create ()
{
    gameScene = this;
    ////////////////////
    // game grid test //
    ////////////////////
    grid = new GameGrid(scene=this, x=0, y=0, width=config.scale.width, height=config.scale.height, rows=20, columns=1);
    // // const cell = grid.getCell(row=2, column=3);
    // grid.setColor(row=2, column=3, color=0xff0000); // red 
    // grid.setColor(row=0, column=0, color=0x131aeb); // blue
    // grid.setColor(row=7, column=7, color=0x32a852); // green




    /////////////////
    // player test //
    /////////////////
    if (navigator.userAgent.indexOf("Firefox") != -1){
        ws.onopen = function (event) {
            console.log("sending firefox");
            ws.send(JSON.stringify({ type: "new_user" }));
        }
    }else{
        console.log("sending chrome");
        ws.send(JSON.stringify({ type: "new_user" }));
    }
    // players = [new Player(scene=this, x=0 * grid.cellHeight, y=0 * grid.cellHeight, width=grid.cellWidth, height=grid.cellHeight, speed=grid.cellHeight, color=0xff0000, "down")]
    // console.log(players)
}

function isCollision(pos,collidables){
    for (let i = 0; i < collidables.length; i++){
        if (pos.x == collidables[i].x && pos.y == collidables[i].y){
            return true
        }
    }
    return false
}

function updateClaimed(player){
    claim_ready = false
    for (let i = 0; i < player.path_tiles.length; i++){
        if(isCollision(player.path_tiles[i],player.claimed_tiles)){
            claim_ready = true
            break
        }
    }
    if(claim_ready == false){
        return
    }
    x_bounds = [1000,0] //format [min,max]
    y_bounds = [1000,0] //format [min,max]
    for (let i = 0; i < player.path_tiles.length; i++){

        //determine min and max for x
        if (player.path_tiles[i].x < x_bounds[0]){
            x_bounds[0] = player.path_tiles[i].x
        }
        if (player.path_tiles[i].x > x_bounds[1]){
            x_bounds[1] = player.path_tiles[i].x
        }

        //determine min and max for y
        if (player.path_tiles[i].y < y_bounds[0]){
            y_bounds[0] = player.path_tiles[i].y
        }
        if (player.path_tiles[i].y > y_bounds[1]){
            y_bounds[1] = player.path_tiles[i].y
        }
    }
    
    for (let x = x_bounds[0]; x < x_bounds[1]; x++){
        for (let y = y_bounds[0]; y < y_bounds[1]; y++){
            if (player.claimed_tiles.indexOf([x,y]) === -1){
                player.claimed_tiles.push([x,y])
            }
        }
    }
}
counter = 0;
function update ()
{   
    // if (players.length < Object.keys(clients).length){
    //     players = [];
    //     for (var [key,value] of Object.entries(clients)){
    //         players.push(new Player(scene=this, x=value.x * grid.cellHeight, y=value.y * grid.cellHeight, width=grid.cellWidth, height=grid.cellHeight, speed=grid.cellHeight, color=0xff0000, "down"));
    //     }
    // }

    // Update the values of the players using data retrieved from server
    if(counter == 0){
        for (let [key,value] of Object.entries(players)){
            value.update();
        }
    }
    counter++
    if(counter >= 5){
        counter = 0;
    }

    // Send only the clients data to server
    
    if (currentPlayer){
        currentPlayer.update();
        // console.log(currentPlayer.winner);
        if (!currentPlayer.allowMove){
            ws.send(JSON.stringify({ event: "ping", type: "check_opponent" }))
        }else if (currentPlayer.winner){
            ws.send(JSON.stringify({ event: "ping", type: "winner" }));
            currentPlayer.winner = false;
        }else{
            ws.send(JSON.stringify({event: "ping", "x": currentPlayer.x, "y": currentPlayer.y}));
        }
    }
}

ws.onmessage = function(wsMessage){
    const message = JSON.parse(wsMessage.data);
    // console.log(message)

    // TODO: handle winner and loser prompts
    // When a new_user is detected, set the currentPlayer variable to reference its IP
    if (message.infoType == "allow_move"){
        document.getElementById("noOpponent").style.display = "none";
        currentPlayer.allowMove = true;
    }else if (message.infoType == "opponent_left"){
        document.getElementById("noOpponent").style.display = "unset";
        document.getElementById("opponentDisconnect").style.display = "unset";
    }else if (message.infoType == "winner"){
        //console.log("You won!");
        document.getElementById("result").innerHTML = "You won! :)";
        document.getElementById("resultBox").style.display = "unset";
    }else if (message.infoType == "loser"){
        //console.log("You lost!");
        document.getElementById("result").innerHTML = "You lost... :(";
        document.getElementById("resultBox").style.display = "unset";
    }else if (message.infoType == "new_user"){
        currentPlayer = new Player(scene=gameScene, x=message.x * grid.cellHeight, y=message.y * grid.cellHeight, width=grid.cellWidth, height=grid.cellHeight, speed=10, color=0x3c58a9, "down");
    }else if (players[message.client]){
        players[message.client].setGridCoords(message.x, message.y);
    }else{
        players[message.client] = new OtherPlayer(scene=gameScene, x=message.x *grid.cellHeight, y=message.y*grid.cellHeight, width=grid.cellWidth, height=grid.cellHeight, color=0x3c58a9)
    }
}

ws.onerror = function(error) {
    console.log('WebSocket error: ' + error);
};