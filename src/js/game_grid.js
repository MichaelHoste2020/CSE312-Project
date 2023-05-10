class GameGrid {
    constructor(scene, x, y, width, height, rows, columns) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.rows = rows;
        this.columns = columns;
        this.cellWidth = width / columns;
        this.cellHeight = height / rows;

        // Create the grid
        this.grid = [];
        for (let i = 0; i < rows; i++) {
        this.grid[i] = [];
        for (let j = 0; j < columns; j++) {
            const graphics = this.scene.add.graphics();
            graphics.lineStyle(1, 0xffffff);
            graphics.strokeRect(this.x + j * this.cellWidth, this.y + i * this.cellHeight, this.cellWidth, this.cellHeight);
            this.grid[i][j] = graphics;
        }
        }
    }

    getCell(row, column) {
        return this.grid[row][column];
    }

    setColor(row, column, color) {
        this.grid[row][column].fillStyle(color, 1);
        this.grid[row][column].fillRect(this.x + column * this.cellWidth, this.y + row * this.cellHeight, this.cellWidth, this.cellHeight);
    }

}