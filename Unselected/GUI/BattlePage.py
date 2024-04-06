import tkinter as tk

# Colors
WHITE = "#ffffff"
BLACK = "#000000"
GRAY = "#cccccc"
RED = "#ff0000"

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class TetrisUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris Start Page")
        self.setup_ui()

    def setup_ui(self):
        # Create canvas
        self.canvas = tk.Canvas(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=WHITE)
        self.canvas.pack()

        # Draw Tetris grids (placeholders)
        self.draw_tetris_grid(25, 50)
        self.draw_tetris_grid(SCREEN_WIDTH // 2 + 25, 50)

        # Draw vertical line in the middle
        self.canvas.create_line(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT, width=2, fill=BLACK)

        # Draw "Next Shape" boxes
        self.draw_next_shape_box(325, 75)
        self.draw_next_shape_box(SCREEN_WIDTH // 2 + 325, 75)

        # Draw labels
        self.create_text_and_label(375, 300, "Your Score", 320)
        self.create_text_and_label(375, 450, "Timer", 470)
        self.create_text_and_label(SCREEN_WIDTH // 2 + 375, 300, "Opponent Score", 320)
        self.create_text_and_label(SCREEN_WIDTH // 2 + 375, 450, "Opponent Timer", 470)

    def draw_tetris_grid(self, x, y):
        self.canvas.create_rectangle(x, y, x + 10 * 25, y + 20 * 25, outline=GRAY)

    def draw_next_shape_box(self, x, y):
        self.canvas.create_rectangle(x, y, x + 100, y + 100, outline=GRAY)

    def create_text_and_label(self, x, y, text, label_y):
        self.canvas.create_text(x, y, text=text, fill=BLACK, font=("Helvetica", 16, "bold"))
        label = tk.Label(self, text="0", font=("Helvetica", 16, "bold"))
        label.place(x=x, y=label_y)

if __name__ == "__main__":
    app = TetrisUI()
    app.mainloop()
