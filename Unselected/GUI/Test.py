import tkinter as tk
from tkinter import font as tkfont

# Colors
WHITE = "#ffffff"
BLACK = "#000000"
GRAY = "#cccccc"
RED = "#ff0000"

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class TetrisStartPage(tk.Tk):
    def __init__(self, font=None):
        super().__init__()
        self.title("Tetris Start Page")
        self.font = font

        # Create canvas
        self.canvas = tk.Canvas(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=WHITE)
        self.canvas.pack()

        # Draw Tetris Gird (Placeholder)
        self.canvas.create_rectangle(100, 50, 100 + 10 * 25, 50 + 20 * 25, fill=GRAY, outline="")

        # Draw Title
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.canvas.create_text(750, 150, text="Tetris Online", font=title_font, fill=BLACK)

        # Draw buttons
        self.draw_buttons()

    def draw_buttons(self):
        # Draw "Start a Game" button
        start_button = tk.Button(self, text="Start a Game", font=self.font, command=self.go_to_create_game)
        start_button.place(x=650, y=225, width=200, height=50)

        # Draw "Join a Game" button
        join_button = tk.Button(self, text="Join a Game", font=self.font, command=self.go_to_player_connect)
        join_button.place(x=650, y=300, width=200, height=50)

        # Draw "Exit" button
        exit_button = tk.Button(self, text="Exit", font=self.font, command=self.quit)
        exit_button.place(x=650, y=375, width=200, height=50)

    def go_to_create_game(self):
        self.hide()
        create_game_page = CreateGamePage(self)
        create_game_page.show()

    def go_to_player_connect(self):
        self.hide()
        player_connect_page = PlayerConnectPage(self)
        player_connect_page.show()

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

class CreateGamePage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Create a Game")
        # (Your initialization code...)

        # Draw labels, buttons, etc.
        self.draw_labels()
        self.draw_buttons()

    def draw_labels(self):
        # Draw labels
        player_ip_label = tk.Label(self, text="Player IP:", font=font)
        player_ip_label.pack()

        invite_code_label = tk.Label(self, text="Invite Code:", font=font)
        invite_code_label.pack()

    def draw_buttons(self):
        # Draw "Create Game" button
        create_button = tk.Button(self, text="Create Game", font=font, command=self.go_to_battle_page)
        create_button.pack()

        # Draw "Go Back" button
        back_button = tk.Button(self, text="Back", font=font, command=self.go_back)
        back_button.pack()

    def go_to_battle_page(self):
        self.hide()
        battle_page = BattlePage(self)
        battle_page.show()

    def go_back(self):
        self.destroy()
        self.master.show()

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

class PlayerConnectPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Connect to Another Player")
        # (Your initialization code...)

        # Draw labels, buttons, etc.
        self.draw_labels()
        self.draw_buttons()

    def draw_labels(self):
        # Draw labels
        player_ip_label = tk.Label(self, text="Player IP:", font=font)
        player_ip_label.pack()

        invite_code_label = tk.Label(self, text="Invite Code:", font=font)
        invite_code_label.pack()

    def draw_buttons(self):
        # Draw "Join Battle" button
        join_button = tk.Button(self, text="Join Battle", font=font, command=self.go_to_battle_page)
        join_button.pack()

        # Draw "Go Back" button
        back_button = tk.Button(self, text="Back", font=font, command=self.go_back)
        back_button.pack()

    def go_to_battle_page(self):
        self.hide()
        battle_page = BattlePage(self)
        battle_page.show()

    def go_back(self):
        self.destroy()
        self.master.show()

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

class BattlePage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Tetris Battle Page")
        # (Your initialization code...)

        # Draw labels, buttons, etc.
        self.draw_labels()
        self.draw_buttons()

    def draw_labels(self):
        # Draw labels
        your_score_label = tk.Label(self, text="Your Score:", font=font)
        your_score_label.pack()

        opponent_score_label = tk.Label(self, text="Opponent Score:", font=font)
        opponent_score_label.pack()

    def draw_buttons(self):
        # Draw "Back" button
        back_button = tk.Button(self, text="Back", font=font, command=self.go_back)
        back_button.pack()

    def go_back(self):
        self.destroy()
        self.master.show()

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

if __name__ == "__main__":
    app = TetrisStartPage()
    font = tkfont.Font(family="Helvetica", size=14)
    app.mainloop()
