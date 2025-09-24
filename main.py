import tkinter as tk
from playerentry import PlayerEntry

def main():
    root = tk.Tk()
    root.title("Photon - Player Entry")
    root.geometry("1300x800")

    # creates player entry frame
    player_entry_screen = PlayerEntry(root)
    player_entry_screen.pack(expand=True, fill = "both")

    root.mainloop()

if __name__ == "__main__":
    main()