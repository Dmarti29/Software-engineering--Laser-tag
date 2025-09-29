import tkinter as tk
from frontend.splashscreen import splash_screen
from frontend.player_entry.player_entry_component import PlayerEntryComponent

def show_player_entry_screen(window):
    player_entry_screen = PlayerEntryComponent(window)
    player_entry_screen.pack(expand=True, fill="both")

    player_entry_screen.update_idletasks()

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")

    splash_screen(window, show_player_entry_screen)

    window.mainloop()

if __name__ == "__main__":
    main()