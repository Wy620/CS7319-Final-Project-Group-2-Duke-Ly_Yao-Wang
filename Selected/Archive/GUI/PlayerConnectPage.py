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

class UI(tk.Tk):
    def __init__(self, master):
        self.master = master
        master.title("Connect to Another Player")

        # Set window size
        master.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        # Font
        self.font = tkfont.Font(family="Helvetica", size=14)

        # Draw UI elements
        self.draw_elements()

    def draw_elements(self):
        # Draw "Connect to another player" text centered at the top
        connect_label = tk.Label(self.master, text="Connect to another player", font=tkfont.Font(family="Helvetica", size=20))
        connect_label.place(x=SCREEN_WIDTH // 2, y=50, anchor="center")

        # Draw labels
        player_ip_label = tk.Label(self.master, text="Player IP:", font=self.font)
        player_ip_label.place(x=50, y=150, anchor="nw")

        invite_code_label = tk.Label(self.master, text="Invite Code:", font=self.font)
        invite_code_label.place(x=50, y=200, anchor="nw")

        # Draw "Join Battle" button
        join_button = tk.Button(self.master, text="Join Battle", font=self.font, command=self.join_battle)
        join_button.place(x=750, y=175, width=150, height=50)

        # Draw "Go Back" button
        back_button = tk.Button(self.master, text="Back", font=self.font, command=self.go_back)
        back_button.place(x=50, y=500, width=150, height=50)

        # Text input boxes
        self.player_ip_input = TextInputBox(self.master, 300, 150, 300, 32)
        self.invite_code_input = TextInputBox(self.master, 300, 200, 300, 32)

    def join_battle(self):
        print("Joining battle...")
        player_ip = self.player_ip_input.get_text()
        invite_code = self.invite_code_input.get_text()
        # Implement the functionality for "Join Battle" button click here

    def go_back(self):
        print("Going back...")
        # Implement the functionality for "Go Back" button click here
        self.master.destroy()  # Close the current window

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

def main():
    root = tk.Tk()
    app = UI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
