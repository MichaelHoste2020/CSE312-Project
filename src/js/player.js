class Player extends Phaser.GameObjects.Sprite {
    constructor(scene, x, y, width, height, speed, color, direction) { 
        // Create a texture with the specified color
        const graphics = new Phaser.GameObjects.Graphics(scene);    
        graphics.fillStyle(color, 1);
        graphics.fillRect(0, 0, width, height); 
        const texture = graphics.generateTexture('player', width, height);
        graphics.destroy(); 
        

        // Fill in superclass constructors using the newly generated texture
        super(scene, x, y, 'player');
        
        // Align the texture with the sprite
        this.setOrigin(0, 0);

        // Add player to the scene
        scene.add.existing(this);

        // Set the member variables
        this.direction = "down"
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.speed = speed;
        this.color = color;
        const {grid_x, grid_y} = this.getGridCoords();
        this.claimed_tiles = [grid_x, grid_y];
        this.path_tiles = [grid_x, grid_y];
        this.controls = {
            down: scene.input.keyboard.addKey('S'),
        }
        this.winner = false;
        this.allowMove = false;
    }

    setGridCoords(x, y) {
        this.x = x;
        this.y = y;
    }

    getGridCoords() {
        var grid_x = this.x / this.width;
        var grid_y = this.y / this.height;
        return {
            grid_x: grid_x,
            grid_y: grid_y
        };
    }

    update() {
        // Move the player
        const {grid_x, grid_y} = this.getGridCoords();
        const max_rows = 20;
        const max_cols = 20;
        
        if (this.allowMove && this.y < 760 && this.spamCheck && this.controls.down?.isDown) {
            this.y += 10;
            this.spamCheck = false;
        }

        if (this.controls.down?.isUp){
            this.spamCheck = true;
        }

        if (this.y >= 760){
            this.winner = true;
        }

        //this.path_tiles.push([grid_x, grid_y])
        //console.log(this.path_tiles)
    }

}