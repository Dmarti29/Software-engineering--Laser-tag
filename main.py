import sys
import tkinter as tk
from frontend.splashscreen import splash_screen
from frontend.player_entry.player_entry_component import PlayerEntryComponent
from frontend.play_action_screen import PlayActionScreen
from frontend.countdowntimer import CountdownTimer
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

        # hide player entry screen
        player_entry_screen.pack_forget()

        # show countdown timer with images 30-1
        countdown_images = [f"frontend/assets/{i}.tif" for i in range(30, 0, -1)]
        
        def show_play_action_after_countdown(window):
            play_action = PlayActionScreen(window, red_team_players, green_team_players)
            play_action.pack(expand=True, fill="both")
        
        CountdownTimer(window, countdown_images, duration=1, next_screen=show_play_action_after_countdown)

    # bind start game click
    player_entry_screen.start_button.config(command=start_play_action_screen)

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")

    time_duration = 30 # default for pressing start game
    if len(sys.argv) > 1:
        try:
            time_duration = float(sys.argv[1])
        except ValueError:
            print("Invalid duration argument. Using default 2 seconds.")
    splash_images = [f"frontend/assets/{i}.tif" for i in range(31)]

    splash_screen(window, show_player_entry_screen)

    window.mainloop()

if __name__ == "__main__":
    main()