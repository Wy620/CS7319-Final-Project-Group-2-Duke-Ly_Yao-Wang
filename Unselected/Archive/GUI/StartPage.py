import tkinter as tk
from tkinter import font
import sys

# Constants
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#C8C8C8"
RED = "#FF0000"

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTONS = [
    {"text": "Start a Game", "command": "start_game"},
    {"text": "Join a Game", "command": "join_game"},
    {"text": "Exit", "command": "exit"}
]

class TetrisUI(tk.Tk):
    def __init__(self, master):
        self.master = master
        master.title("Tetris Start Page")

        # Create canvas
        self.canvas = tk.Canvas(master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()

        self.draw_elements()
        self.bind_events()

    def draw_elements(self):
        self.draw_tetris_grid()
        self.draw_buttons()
        self.draw_title()

    def draw_tetris_grid(self):
        self.canvas.create_rectangle(100, 50, 100 + 10 * 25, 50 + 20 * 25, fill=GRAY, outline="")

    def draw_buttons(self):
        for idx, button_info in enumerate(BUTTONS):
            y = 250 + idx * (BUTTON_HEIGHT + 10)
            self.draw_button(650, y, button_info["text"])

    def draw_button(self, x, y, text):
        self.canvas.create_rectangle(x, y, x + BUTTON_WIDTH, y + BUTTON_HEIGHT, fill=GRAY, outline="")
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        text_x = x + BUTTON_WIDTH / 2
        text_y = y + BUTTON_HEIGHT / 2
        self.canvas.create_text(text_x, text_y, text=text, font=button_font, fill=BLACK)

    def draw_title(self):
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.canvas.create_text(650 + BUTTON_WIDTH / 2, 150, text="Tetris Online", font=title_font, fill=BLACK)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y
        for idx, button_info in enumerate(BUTTONS):
            button_y = 250 + idx * (BUTTON_HEIGHT + 10)
            if 650 < x < 650 + BUTTON_WIDTH and button_y < y < button_y + BUTTON_HEIGHT:
                command = getattr(self, button_info["command"], None)
                if command:
                    command()
                break

class TetrisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.ui = TetrisUI(self.root)

    def start_game(self):
        print("Starting a new game...")
        # Implement your start game logic here

    def join_game(self):
        print("Joining a game...")
        # Implement your join game logic here

    def exit(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()

def main():
    app = TetrisApp()
    app.run()
    sys.exit()

if __name__ == "__main__":
    main()
