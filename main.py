import tkinter as tk
from splashscreen import splash_screen
from playerentry import PlayerEntry

def show_player_entry_screen(window):
    # creates player entry frame
    player_entry_screen = PlayerEntry(window)
    player_entry_screen.pack(expand=True, fill = "both")

    #updates layout
    player_entry_screen.update_idletasks()

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")

    splash_screen(window, show_player_entry_screen)

    window.mainloop()

if __name__ == "__main__":
    main()