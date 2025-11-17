import sys
import tkinter as tk
import pygame
import random
from frontend.splashscreen import splash_screen
from frontend.player_entry.player_entry_component import PlayerEntryComponent
from frontend.play_action_screen import PlayActionScreen
from frontend.countdowntimer import CountdownTimer

# Music functions
def init_music(track_number):
    """Initialize pygame mixer and load a specific track"""
    pygame.mixer.init()
    pygame.mixer.music.load(f"photon_tracks/Track0{track_number}.mp3")
    pygame.mixer.music.set_volume(0.4)

def start_music():
    """Start playing music in loop"""
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

def stop_music():
    """Stop playing music"""
    pygame.mixer.music.stop()

# start up the player entry screen
def show_player_entry_screen(window):
    player_entry_screen = PlayerEntryComponent(window)
    player_entry_screen.pack(expand=True, fill="both")

    player_entry_screen.update_idletasks()

    # starts the game and switches to play action screen
    def start_play_action_screen():
        # Don't call start_game() here - it broadcasts 202 immediately!
        # We'll broadcast 202 AFTER the 30-second countdown finishes
        
        # retrieve player names
        red_team_players = player_entry_screen.get_red_team_data()["players"]
        green_team_players = player_entry_screen.get_green_team_data()["players"]

        # hide player entry screen
        player_entry_screen.pack_forget()

        # show countdown timer with images 30-1
        countdown_images = [f"frontend/assets/{i}.tif" for i in range(30, 0, -1)]
        
        # Schedule music to start 15.4 seconds after countdown begins
        window.after(15400, start_music)
        
        # Schedule music to stop after game ends (6 minutes + 30 seconds countdown = 390 seconds)
        window.after(390000, stop_music)
        
        def show_play_action_after_countdown(window):
            # Countdown finished! Now load the play action screen first
            
            def return_to_entry():
                """Return to player entry screen"""
                # Stop music if playing
                stop_music()
                # Hide play action screen
                for widget in window.winfo_children():
                    widget.pack_forget()
                # Show player entry screen again
                show_player_entry_screen(window)
            
            play_action = PlayActionScreen(window, red_team_players, green_team_players, return_callback=return_to_entry)
            play_action.pack(expand=True, fill="both")
            
            # AFTER screen is loaded, broadcast code 202 to start traffic generator
            # Delay slightly to ensure screen is fully rendered
            def broadcast_start():
                try:
                    import requests
                    requests.post("http://localhost:5000/game/start", timeout=1)
                    print("Game started - code 202 broadcasted")
                except Exception as e:
                    print(f"Failed to start game: {e}")
            
            window.after(1150, broadcast_start)  # 1.15 second delay to ensure screen is ready
        
        CountdownTimer(window, countdown_images, duration=1, next_screen=show_play_action_after_countdown)

    # bind start game click
    player_entry_screen.start_button.config(command=start_play_action_screen)

def main():
    window = tk.Tk()
    window.title("Photon - Player Entry")
    window.geometry("1300x800")
    
    # Initialize music with random track (1-8)
    random_track = random.randint(1, 8)
    init_music(random_track)

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