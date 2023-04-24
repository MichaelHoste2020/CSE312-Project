class Player extends Phaser.GameObjects.Sprite {
    constructor(scene, x, y, width, height, speed, color) { 
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
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.speed = speed;
        this.color = color;
        this.claimed_tiles = [];
        this.path_tiles = [];
        this.controls = {
            up: scene.input.keyboard.addKey('W'),
            left: scene.input.keyboard.addKey('A'),
            down: scene.input.keyboard.addKey('S'),
            right: scene.input.keyboard.addKey('D')
        }
    }


    update() {
        // Control the player
        if (this.controls.up?.isDown) {
            this.y -= this.speed;
        }
        if (this.controls.left?.isDown) {
            this.x -= this.speed;
        }
        if (this.controls.down?.isDown) {
            this.y += this.speed;
        }
        if (this.controls.right?.isDown) {
            this.x += this.speed;
        }
    }

}