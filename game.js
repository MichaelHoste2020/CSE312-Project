////////////
// Canvas //
////////////
function initializeCanvas() {
    canvas = document.getElementById("myCanvas");
    ctx = canvas.getContext("2d");
}

function setCanvasSize() {
    var width = window.innerWidth;
    var height = window.innerHeight;

    var boxSize = Math.min(width, height) * 0.975;
    
    canvas.width = boxSize;
    canvas.height = boxSize;
}

////////////
// Player //
////////////
class Player {
    constructor(pos, size, color, speed) {
        this.pos = pos;
        this.size = size;
        this.color = color;
        this.speed = speed;
    }

    draw() {
        ctx.fillStyle = "rgb(" + this.color.toString() + ")";
        ctx.fillRect(this.pos[0], this.pos[1], this.size[0], this.size[1]);
    }
    
}

// Get Input - For Controlling P1
document.addEventListener("keydown", (event) => {
    if(event.key == "w") {
        p1.pos[1] -= p1.speed;
    }
    else if(event.key == "a") {
        p1.pos[0] -= p1.speed;
    }
    else if(event.key == "s") {
        p1.pos[1] += p1.speed;
    }
    else if(event.key == "d") {
        p1.pos[0] += p1.speed;
    }
});

//////////
// Game //
//////////
function startGame() {
    // Get a reference to the canvas and set its size according to the window
    initializeCanvas();
    setCanvasSize();

    // Create the player
    p1 = new Player(pos=[0,0], size=[100,100], color=[0,0,255], speed=10);

    // Start the game loop
    window.requestAnimationFrame(gameLoop);
}

function gameLoop() {
    // clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw game elements to the screen
    p1.draw();

    // continue the game loop
    window.requestAnimationFrame(gameLoop);
}

