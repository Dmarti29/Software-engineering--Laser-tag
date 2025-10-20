import tkinter as tk
from PIL import Image, ImageTk

class CountdownTimer:
    def __init__(self, window, images, duration, next_screen=None):
        self.window = window
        self.images = images
        self.duration = duration * 1000
        self.next_screen = next_screen
        self.index = 0
        self.frame = tk.Frame(window)
        self.frame.pack(expand=True, fill="both")
        self.label = tk.Label(self.frame)
        self.label.pack(expand=True)
        self._show_next_image()

    def _show_next_image(self):
        if self.index < len(self.images):
            img = Image.open(self.images[self.index])
            img = img.resize((1300, 800))
            photo = ImageTk.PhotoImage(img)
            self.label.config(image=photo)
            self.label.image = photo
            self.index += 1
            self.window.after(self.duration, self._show_next_image)
        else:
            self.frame.destroy()
            if self.next_screen:
                self.next_screen(self.window)