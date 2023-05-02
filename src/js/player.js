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
            up: scene.input.keyboard.addKey('W'),
            left: scene.input.keyboard.addKey('A'),
            down: scene.input.keyboard.addKey('S'),
            right: scene.input.keyboard.addKey('D')
        }
    }

    setGridCoords(x, y) {
        this.x = x;
        this.y = y;
    }

    getGridCoords() {
        var grid_x = Math.round(this.x / this.width);
        var grid_y = Math.round(this.y / this.height);
        return {
            grid_x: grid_x,
            grid_y: grid_y
        };
    }

    update() {
        // Control the player
        if (this.controls.up?.isDown) {
            this.direction = "up"
        }
        if (this.controls.left?.isDown) {
            this.direction = "left"
        }
        if (this.controls.down?.isDown) {
            this.direction = "down"
        }
        if (this.controls.right?.isDown) {
            this.direction = "right"
        }

        // Move the player
        const {grid_x, grid_y} = this.getGridCoords();
        const max_rows = 20;
        const max_cols = 20;

        if (grid_x > 0 && this.direction == "left") {
            this.x -= this.speed;       
        }
        else if (grid_x < (max_cols - 1) && this.direction == "right") {
            this.x += this.speed;
        }
        if (grid_y > 0 && this.direction == "up") {
            this.y -= this.speed;
        }
        if (grid_y < (max_rows - 1) && this.direction == "down") {
            this.y += this.speed;
        }

        this.path_tiles.push([grid_x, grid_y])
    }

}