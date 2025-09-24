import tkinter as tk
from playerentry import PlayerEntry

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")

    # creates player entry frame
    player_entry_screen = PlayerEntry(window)
    player_entry_screen.pack(expand=True, fill = "both")

    window.mainloop()

if __name__ == "__main__":
    main()