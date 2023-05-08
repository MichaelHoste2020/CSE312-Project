class OtherPlayer extends Phaser.GameObjects.Sprite {
    constructor(scene, x, y, width, height, color) { 
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
        this.color = color;
    }

    setGridCoords(x, y) {
        this.x = x;
        this.y = y;
    }
}