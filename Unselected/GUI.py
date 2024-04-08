import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from threading import Thread
from Network import Ipv4Checker
from Network import Peer
from Game_Logic import TetrisGUI, NextShapeWindow
from Game_Logic import TetrisGame

# Colors
WHITE = "#ffffff"
BLACK = "#000000"
GRAY = "#cccccc"
RED = "#ff0000"

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Buttons dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

SCALE = 25


class TetrisStartPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris Start Page")
        self.font = tkfont.Font(family="Helvetica", size=14)

        # Create canvas
        self.canvas = tk.Canvas(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg=WHITE)
        self.canvas.pack()

        # Draw Tetris Gird (Placeholder)
        self.canvas.create_rectangle(100, 50, 100 + 10 * SCALE, 50 + 20 * SCALE, fill=GRAY, outline="")

        # Draw Title
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.canvas.create_text(750, 150, text="Tetris Online", font=title_font, fill=BLACK)

        # Draw buttons
        self.draw_buttons()

    def draw_buttons(self):
        # Draw "Start a Game" button
        start_button = tk.Button(self, text="Start a Game", font=self.font, command=self.go_to_create_game)
        start_button.place(x=650, y=225, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        # Draw "Join a Game" button
        join_button = tk.Button(self, text="Join a Game", font=self.font, command=self.go_to_player_connect)
        join_button.place(x=650, y=300, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        # Draw "Exit" button
        exit_button = tk.Button(self, text="Exit", font=self.font, command=self.quit)
        exit_button.place(x=650, y=375, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

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


class TextInputBox:
    def __init__(self, master, x, y, width, height):
        self.frame = tk.Frame(master, highlightbackground=GRAY, highlightthickness=2)
        self.frame.place(x=x, y=y, width=width, height=height)
        self.entry = tk.Entry(self.frame, font=tkfont.Font(family="Helvetica", size=14))
        self.entry.pack(fill="both", expand=True)
        self.entry.bind("<FocusIn>", lambda event: self.frame.config(highlightbackground=GRAY))
        self.entry.bind("<FocusOut>", lambda event: self.frame.config(highlightbackground=WHITE))

    def get_text(self):
        return self.entry.get()

    def set_text(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)


class CreateGamePage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Create a Game")
        self.peer = None

        # Set window size
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        # Draw UI elements
        self.draw_elements()

    def draw_elements(self):
        # Draw "Connect to another player" text centered at the top
        connect_label = tk.Label(self, text="Create a Game", font=tkfont.Font(family="Helvetica", size=20))
        connect_label.place(x=SCREEN_WIDTH // 2, y=50, anchor="center")

        # Draw labels
        player_ip_label = tk.Label(self, text="Player IP:", font=tkfont.Font(family="Helvetica", size=14))
        player_ip_label.place(x=50, y=150, anchor="nw")

        invite_code_label = tk.Label(self, text="Invite Code:", font=tkfont.Font(family="Helvetica", size=14))
        invite_code_label.place(x=50, y=200, anchor="nw")

        # Draw "Create Game" button
        create_button = tk.Button(self, text="Create Game", font=tkfont.Font(family="Helvetica", size=14),
                                  command=self.go_to_battle_page)
        create_button.place(x=750, y=175, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        # Draw "Go Back" button
        back_button = tk.Button(self, text="Back", font=tkfont.Font(family="Helvetica", size=14), command=self.go_back)
        back_button.place(x=50, y=500, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        # Text input boxes
        self.player_ip_input = TextInputBox(self, 300, 150, 300, 32)
        self.invite_code_input = TextInputBox(self, 300, 200, 300, 32)

        current_ip = Ipv4Checker()
        self.player_ip_input.set_text(current_ip.get_ipv4_address())
        self.invite_code_input.set_text("ABCDE")

    def go_to_battle_page(self):
        self.peer = Peer(self.player_ip_input.get_text(), self.invite_code_input.get_text())
        Thread(target=self.peer.start_accepting_connections).start()
        self.hide()
        battle_page = BattlePage(self, self.peer)
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
        self.peer = None

        # Set window size
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        # Font
        self.font = tkfont.Font(family="Helvetica", size=14)

        # Draw UI elements
        self.draw_elements()

    def draw_elements(self):
        # Draw "Connect to another player" text centered at the top
        connect_label = tk.Label(self, text="Connect to another player", font=tkfont.Font(family="Helvetica", size=20))
        connect_label.place(x=SCREEN_WIDTH // 2, y=50, anchor="center")

        # Draw labels
        player_ip_label = tk.Label(self, text="Player IP:", font=self.font)
        player_ip_label.place(x=50, y=150, anchor="nw")

        invite_code_label = tk.Label(self, text="Invite Code:", font=self.font)
        invite_code_label.place(x=50, y=200, anchor="nw")

        invite_code_label = tk.Label(self, text="Opponent IP:", font=self.font)
        invite_code_label.place(x=50, y=250, anchor="nw")

        # Draw "Join Battle" button
        join_button = tk.Button(self, text="Join Battle", font=self.font, command=self.go_to_battle_page)
        join_button.place(x=750, y=175, width=150, height=50)

        # Draw "Go Back" button
        back_button = tk.Button(self, text="Back", font=self.font, command=self.go_back)
        back_button.place(x=50, y=500, width=150, height=50)

        # Text input boxes
        self.player_ip_input = TextInputBox(self, 300, 150, 300, 32)
        self.invite_code_input = TextInputBox(self, 300, 200, 300, 32)
        self.opponent_ip_input = TextInputBox(self, 300, 250, 300, 32)

        current_ip = Ipv4Checker()
        self.player_ip_input.set_text(current_ip.get_ipv4_address())
        self.invite_code_input.set_text("ABCDE")

    def go_to_battle_page(self):
        self.peer = Peer(self.player_ip_input.get_text(), self.invite_code_input.get_text())
        Thread(target=self.peer.connect(self.opponent_ip_input.get_text(), self.invite_code_input.get_text())).start()
        #self.peer.connect(self.opponent_ip_input.get_text(), self.invite_code_input.get_text())
        self.hide()
        battle_page = BattlePage(self, self.peer)
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
    def __init__(self, master, peer):
        super().__init__(master)
        self.title("Tetris Battle Page")
        self.peer = peer
        self.player_score_label = None
        self.player_timer_label = None
        self.opponent_score_label = None
        self.opponent_timer_label = None
        self.time_limit = 360 * 1000  # 360s in ms

        self.setup_ui()

        cell_size = 25  # Define cell_size here

        # Initialize the Opponent Tetris Game Window
        self.opponentGame = TetrisGame(self, 10, 20, cell_size, peer)
        self.opponentTetrisGui = TetrisGUI(self, self.opponentGame, cell_size)

        # Initialize the Player Tetris Game Window
        self.playerGame = TetrisGame(self, 10, 20, cell_size, peer)
        self.playerTetrisGui = TetrisGUI(self, self.playerGame, cell_size)

        # Place Player Tetris GUI on the canvas
        self.playerTetrisGui.canvas.place(x=25, y=50)

        # Place Opponent Tetris GUI on the canvas
        self.opponentTetrisGui.canvas.place(x=SCREEN_WIDTH // 2 + 25, y=50)

        # Initialize Player Next Shape window
        self.playerNextShapeBox = NextShapeWindow(self, 16.5)
        self.playerTetrisGui.next_shape_window = self.playerNextShapeBox

        # Initialize Opponent Next Shape window
        self.opponentNextShapeBox = NextShapeWindow(self, 16.5)
        self.opponentTetrisGui.next_shape_window = self.opponentNextShapeBox

        # Place Player Next Shape window on the canvas
        self.playerNextShapeBox.canvas.place(x=325, y=75)

        # Place Opponent Next Shape window on the canvas
        self.opponentNextShapeBox.canvas.place(x=SCREEN_WIDTH // 2 + 325, y=75)

        self.refresh_timer()  # Start timer

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
        self.canvas.create_text(375, 50, text="Next Shape", fill=BLACK, font=("Helvetica", 16, "bold"))
        self.draw_next_shape_box(325, 75)
        self.canvas.create_text(SCREEN_WIDTH // 2 + 375, 50, text="Next Shape", fill=BLACK,
                                font=("Helvetica", 16, "bold"))
        self.draw_next_shape_box(SCREEN_WIDTH // 2 + 325, 75)

        # Draw labels
        self.player_score_label = self.create_text_and_label(375, 300, "Your Score", 320)
        self.player_timer_label = self.create_text_and_label(375, 450, "Timer", 470)
        self.opponent_score_label = self.create_text_and_label(SCREEN_WIDTH // 2 + 400, 300, "Opponent Score", 320)
        self.opponent_timer_label = self.create_text_and_label(SCREEN_WIDTH // 2 + 400, 450, "Opponent Timer", 470)

    def draw_tetris_grid(self, x, y):
        self.canvas.create_rectangle(x, y, x + 10 * 25, y + 20 * 25, outline=GRAY)

    def draw_next_shape_box(self, x, y):
        self.canvas.create_rectangle(x, y, x + 100, y + 100, outline=GRAY)

    def create_text_and_label(self, x, y, text, label_y):
        self.canvas.create_text(x, y, text=text, fill=BLACK, font=("Helvetica", 16, "bold"))
        label = tk.Label(self, text="0", font=("Helvetica", 16, "bold"))
        label.place(x=x, y=label_y)
        return label

    def refresh_timer(self):
        if self.time_limit == 0:
            self.playerGame.stop_game()
            self.opponentGame.stop_game()
            self.stop_refresh_timer()
            if self.playerGame.tetris_grid.score > self.opponentGame.tetris_grid.score:
                messagebox.showinfo("Time's up!", "The game is over!\n You won!")
            elif self.playerGame.tetris_grid.score < self.opponentGame.tetris_grid.score:
                messagebox.showinfo("Time's up!", "The game is over!\n You lost!")
            elif self.playerGame.tetris_grid.score == self.opponentGame.tetris_grid.score:
                messagebox.showinfo("Time's up!", "The game is over!\n It is a tie!")
            #self.playerGame.send_last_game_data()
            #self.peer.stop_accepting_connections()

        if self.time_limit < 360000 and self.playerGame.is_game_over == True:
            #self.playerGame.stop_game()
            self.opponentGame.stop_game()
            self.stop_refresh_timer()
            messagebox.showinfo("Game Over", "You lost!")
            #self.playerGame.send_last_game_data()
            #self.peer.stop_accepting_connections()
        elif self.time_limit < 360000 and self.opponentGame.is_game_over == True:
            self.playerGame.stop_game()
            #self.opponentGame.stop_game()
            self.stop_refresh_timer()
            messagebox.showinfo("Game Over", "You won!")
            #self.playerGame.send_last_game_data()
            #self.peer.stop_accepting_connections()

        if self.playerGame.is_game_over == False and self.opponentGame.is_game_over == False and self.time_limit > 0:
            self.player_timer_label.config(text=str(self.time_limit / 1000))
            self.player_score_label.config(text=str(self.playerGame.tetris_grid.score))
            self.opponent_timer_label.config(text=str(self.time_limit / 1000))
            self.opponent_score_label.config(text=str(self.opponentGame.tetris_grid.score))
            self.time_limit -= 100

        self.master.after(100, self.refresh_timer)

    def stop_refresh_timer(self):
        if self.refresh_timer is not None:
            self.master.after_cancel(self.refresh_timer)
            self.refresh_timer = None

    def show(self):
        self.update()
        self.deiconify()
        self.peer.tetris_gui = self.opponentTetrisGui
        while not self.peer.connected:
            #print("Waiting for Connection")
            pass

        self.opponentGame.is_game_over = False
        self.playerGame.start_game()

    def hide(self):
        self.withdraw()


if __name__ == "__main__":
    app = TetrisStartPage()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("GUI application interrupted by user")
