import tkinter as tk
from frontend.splashscreen import splash_screen
from frontend.player_entry.player_entry_component import PlayerEntryComponent
from frontend.play_action_screen import PlayActionScreen

# start up the player entry screen
def show_player_entry_screen(window):
    player_entry_screen = PlayerEntryComponent(window)
    player_entry_screen.pack(expand=True, fill="both")

    player_entry_screen.update_idletasks()

    # starts the game and switches to play action screen
    def start_play_action_screen():
        player_entry_screen.start_game()

        # retrieve player names
        red_team_players = player_entry_screen.get_red_team_data()["players"]
        green_team_players = player_entry_screen.get_green_team_data()["players"]

        play_action = PlayActionScreen(window, red_team_players, green_team_players)

        player_entry_screen.pack_forget()
        play_action.pack(expand=True, fill="both")

    # bind start game click
    player_entry_screen.start_button.config(command=start_play_action_screen)

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")

    splash_screen(window, show_player_entry_screen)

    window.mainloop()

if __name__ == "__main__":
    main()