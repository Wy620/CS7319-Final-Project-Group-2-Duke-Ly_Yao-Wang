# Control Component (K-Component)
import tkinter as tk

class TetrisGUI:
    def __init__(self, master, game, cell_size):
        self.master = master
        self.game = game
        self.cell_size = cell_size
        self.canvas = tk.Canvas(master, width=game.width * cell_size, height=game.height * cell_size, bg='black')
        self.canvas.pack()
        self.game.gui = self
        master.bind('<Key>', self.game.handle_input)
        self.draw_grid()

    def draw_grid(self):
        # Draw grid lines
        for i in range(0, self.game.height * self.cell_size, self.cell_size):
            self.canvas.create_line(0, i, self.game.width * self.cell_size, i, fill="gray")
        for j in range(0, self.game.width * self.cell_size, self.cell_size):
            self.canvas.create_line(j, 0, j, self.game.height * self.cell_size, fill="gray")

    def draw_piece(self):
        self.canvas.delete("piece")
        for y, row in enumerate(self.game.tetris_grid.grid):
            for x, cell in enumerate(row):
                if cell:
                    color = self.game.colors[cell]  # Get color from game's color dictionary
                    canvas_x = x * self.cell_size
                    canvas_y = y * self.cell_size
                    self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.cell_size,
                                                 canvas_y + self.cell_size, fill=color,
                                                 outline="white", tags="piece")
        if self.game.current_piece:
            shape = self.game.current_piece.shape
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        color = self.game.colors[self.game.current_piece.color]  # Access colors from game
                        canvas_x = (self.game.current_piece.x + x) * self.cell_size
                        canvas_y = (self.game.current_piece.y + y) * self.cell_size
                        self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.cell_size,
                                                     canvas_y + self.cell_size, fill=color,
                                                     outline="white", tags="piece")

class TetrisGame:
    DROP_INTERVAL = 500
    RAPID_DROP_INTERVAL = 50  # Define a shorter interval for rapid dropping
    colors = {
        1: 'purple',
        2: 'orange',
        3: 'blue',
        4: 'green',
        5: 'red',
        6: 'cyan',
        7: 'yellow'
    }

    def __init__(self, master, width, height, cell_size):
        self.master = master
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.tetris_grid = TetrisGrid(width, height)
        self.current_piece = None
        self.is_game_over = False
        self.gui = None
        self.drop_timer = None  # Initialize drop timer

    def start_game(self):
        TetriminoShapes.refill_bag()
        self.spawn_piece()
        self.init_drop_timer()  # Start drop timer

    def spawn_piece(self):
        self.tetris_grid.clear_full_rows()
        self.current_piece = TetriminoShapes.get_random_shape_from_bag()
        self.current_piece.x = 4
        self.current_piece.y = -1
        self.update_view()

    def init_drop_timer(self):
        self.drop_timer = self.master.after(self.DROP_INTERVAL, self.drop_piece)

    def reset_drop_timer(self):
        # Cancel current drop timer and start a new one based on the current piece's drop interval
        if self.drop_timer:
            self.master.after_cancel(self.drop_timer)
        if self.is_dropping():
            self.init_drop_timer()

    def stop_drop_timer(self):
        if self.drop_timer:
            self.master.after_cancel(self.drop_timer)
            self.drop_timer = None

    def drop_piece(self):
        if not self.move_piece(0, 1):
            self.stop_drop_timer()  # Stop the drop timer
            self.lock_piece()
            self.spawn_piece()
            if not self.move_piece(0, 1):
                self.is_game_over = True
            else:
                self.drop_piece()  # Recursive call with condition to stop
        else:
            self.reset_drop_timer()  # Reset drop timer for continuous dropping

    def move_piece(self, dx, dy):
        if self.current_piece:
            new_x = self.current_piece.x + dx
            new_y = self.current_piece.y + dy
            if self.is_valid_move(new_x, new_y):
                self.current_piece.move(dx, dy)
                self.update_view()
                return True
        return False

    def handle_input(self, event):
        if event.keysym == 'Left':
            self.move_piece(-1, 0)
        elif event.keysym == 'Right':
            self.move_piece(1, 0)
        elif event.keysym == 'Down':
            self.drop_piece()  # Immediate drop
        elif event.keysym == 'Up':
            self.rotate_piece()

    def is_dropping(self):
        return self.current_piece is not None and not self.is_game_over

    def update_view(self):
        self.gui.draw_piece()
        self.tetris_grid.print_grid()

    def rotate_piece(self):
        if self.current_piece:
            rotated_piece = TetriminoRotator.rotate_clockwise(self.current_piece)
            if self.tetris_grid.is_valid_position(rotated_piece.x, rotated_piece.y) and \
                    self.tetris_grid.is_cell_empty(rotated_piece.x, rotated_piece.y):
                self.current_piece = rotated_piece
                self.update_view()

    def lock_piece(self):
        if self.current_piece:
            if not self.tetris_grid.place_tetrimino(self.current_piece, self.current_piece.x, self.current_piece.y):
                self.is_game_over = True
            self.current_piece = None
            #self.reset_drop_timer()  # Reset drop timer after locking piece

    def is_valid_move(self, x, y):
        for row_index, row in enumerate(self.current_piece.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_x = x + col_index
                    grid_y = y + row_index
                    if not self.tetris_grid.is_valid_position(grid_x, grid_y) or not self.tetris_grid.is_cell_empty(
                            grid_x, grid_y):
                        return False
        return True

# Computation Component (C-Component)
import random

class Tetrimino:
    def __init__(self, shape, color, x=0, y=0):
        self.shape = shape
        self.color = color
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class TetriminoShapes:
    @staticmethod
    def create_T_shape():
        shape = [
            [0, 1, 0],
            [1, 1, 1]
        ]
        return Tetrimino(shape, 1)  # Assigning color purple to T shape

    @staticmethod
    def create_L_shape():
        shape = [
            [1, 0],
            [1, 0],
            [1, 1]
        ]
        return Tetrimino(shape, 2)  # Assigning color orange to L shape

    @staticmethod
    def create_J_shape():
        shape = [
            [0, 1],
            [0, 1],
            [1, 1]
        ]
        return Tetrimino(shape, 3)  # Assigning color blue to J shape

    @staticmethod
    def create_S_shape():
        shape = [
            [0, 1, 1],
            [1, 1, 0]
        ]
        return Tetrimino(shape, 4)  # Assigning color green to S shape

    @staticmethod
    def create_Z_shape():
        shape = [
            [1, 1, 0],
            [0, 1, 1]
        ]
        return Tetrimino(shape, 5)  # Assigning color red to Z shape

    @staticmethod
    def create_I_shape():
        shape = [
            [1],
            [1],
            [1],
            [1]
        ]
        return Tetrimino(shape, 6)  # Assigning color cyan to I shape

    @staticmethod
    def create_O_shape():
        shape = [
            [1, 1],
            [1, 1]
        ]
        return Tetrimino(shape, 7)  # Assigning color yellow to O shape

    shapes_bag = []

    @staticmethod
    def refill_bag():
        TetriminoShapes.shapes_bag = [
            TetriminoShapes.create_T_shape(),
            TetriminoShapes.create_L_shape(),
            TetriminoShapes.create_J_shape(),
            TetriminoShapes.create_S_shape(),
            TetriminoShapes.create_Z_shape(),
            TetriminoShapes.create_I_shape(),
            TetriminoShapes.create_O_shape()
        ]

    @staticmethod
    def get_random_shape_from_bag():
        if not TetriminoShapes.shapes_bag:
            TetriminoShapes.refill_bag()
        return TetriminoShapes.shapes_bag.pop(random.randint(0, len(TetriminoShapes.shapes_bag) - 1))

class TetriminoRotator:
    @staticmethod
    def rotate_clockwise(tetrimino):
        rotated_shape = [[tetrimino.shape[y][x] for y in range(len(tetrimino.shape))] for x in range(len(tetrimino.shape[0]) - 1, -1, -1)]
        tetrimino.shape = rotated_shape  # Update the shape of the current tetrimino
        return tetrimino

    @staticmethod
    def rotate_counter_clockwise(tetrimino):
        rotated_shape = [[tetrimino.shape[y][x] for y in range(len(tetrimino.shape) - 1, -1, -1)] for x in range(len(tetrimino.shape[0]))]
        tetrimino.shape = rotated_shape  # Update the shape of the current tetrimino
        return tetrimino

class TetrisGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def __str__(self):
        grid_representation = ""
        for row in self.grid:
            grid_representation += ''.join(str(cell) if cell else '.' for cell in row) + '\n'  # Use '.' for empty cells
        return grid_representation

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_cell_empty(self, x, y):
        return self.is_valid_position(x, y) and self.grid[y][x] == 0

    def is_row_full(self, row):
        return all(cell != 0 for cell in row)

    def clear_row(self, row):
        self.grid.pop(row)
        self.grid.insert(0, [0] * self.width)

    def clear_full_rows(self):
        rows_to_clear = []
        for i, row in enumerate(self.grid):
            if self.is_row_full(row):
                rows_to_clear.append(i)
        for row_index in rows_to_clear:
            self.clear_row(row_index)

    def place_tetrimino(self, tetrimino, x, y):
        for row_index, row in enumerate(tetrimino.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_x = x + col_index
                    grid_y = y + row_index
                    if not self.is_cell_empty(grid_x, grid_y):
                        return False  # Tetrimino collides with occupied cells
        for row_index, row in enumerate(tetrimino.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    grid_x = x + col_index
                    grid_y = y + row_index
                    self.grid[grid_y][grid_x] = tetrimino.color  # Use Tetrimino's color
        self.clear_full_rows()  # Check and clear full rows after placing tetrimino
        return True

    def print_grid(self):
        print(self)

# Main
root = tk.Tk()
root.title("Tetris")
cell_size = 30  # Define cell_size here
game = TetrisGame(root, 10, 20, cell_size)
tetris_gui = TetrisGUI(root, game, cell_size)
game.start_game()
root.mainloop()
