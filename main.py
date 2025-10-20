import tkinter as tk
from frontend.splashscreen import splash_screen
from frontend.player_entry.player_entry_component import PlayerEntryComponent
from frontend.play_action_screen import PlayActionScreen

def show_player_entry_screen(window):
    player_entry_screen = PlayerEntryComponent(window)
    player_entry_screen.pack(expand=True, fill="both")

    player_entry_screen.update_idletasks()

    play_action = PlayActionScreen(window)

    def start_play_action_screen():
        player_entry_screen.start_game()

        player_entry_screen.pack_forget()
        play_action.pack(expand=True, fill="both")

    player_entry_screen.start_button.config(command=start_play_action_screen)

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")

    splash_screen(window, show_player_entry_screen)

    window.mainloop()

if __name__ == "__main__":
    main()