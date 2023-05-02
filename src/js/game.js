const ws = new WebSocket('ws://' + window.location.host + '/lobby');
var gameScene = null;
var clients = {};

var config = {
    type: Phaser.AUTO,
    scale: {
        mode: Phaser.Scale.FIT,
        parent: 'game-container',
        width: Math.min(window.innerWidth, window.innerHeight),
        height: Math.min(window.innerWidth, window.innerHeight)
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


function preload ()
{
}

function create ()
{
    gameScene = this;
    ////////////////////
    // game grid test //
    ////////////////////
    grid = new GameGrid(scene=this, x=0, y=0, width=config.scale.width, height=config.scale.height, rows=20, columns=20);
    // // const cell = grid.getCell(row=2, column=3);
    grid.setColor(row=2, column=3, color=0xff0000); // red 
    grid.setColor(row=0, column=0, color=0x131aeb); // blue
    grid.setColor(row=7, column=7, color=0x32a852); // green




    /////////////////
    // player test //
    /////////////////
    ws.send(JSON.stringify({ type: "new_user" }));
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

    if(counter == 0){
        //console.log(players)
        for (let [key,value] of Object.entries(players)){
            // console.log(players[i])
            value.update();
            updateClaimed(value);
            ws.send(JSON.stringify({"x": value.x, "y": value.y}))
        }
    }
    counter++
    if(counter >= 5){
        counter = 0;
    }
}

ws.onmessage = function(wsMessage){
    const message = JSON.parse(wsMessage.data);
    console.log(message)
    if (players[message.client]){
        players[message.client].setGridCoords(message.x, message.y);
    }else{
        players[message.client] = new Player(scene=gameScene, x=message.x * grid.cellHeight, y=message.y * grid.cellHeight, width=grid.cellWidth, height=grid.cellHeight, speed=grid.cellHeight, color=0xff0000, "down");
    }
}