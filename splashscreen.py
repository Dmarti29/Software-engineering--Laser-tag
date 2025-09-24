import tkinter as tk
from PIL import Image, ImageTk

def splash_screen(window, next_screen):
    #splash screen frame
    frame = tk.Frame(window)
    frame.pack(expand=True, fill="both")

    #load photon logo
    photon_image = Image.open("assets/logo.jpg")
    photo = ImageTk.PhotoImage(photon_image)

    label = tk.Label(frame, image=photo)
    label.image = photo
    label.pack(expand=True)

    #removes splash screen frame and goes to the next screen
    def show_next_screen():
        frame.destroy()
        next_screen(window)

    window.after(3000, show_next_screen)
