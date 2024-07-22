import tkinter as tk
from PIL import Image, ImageTk
import os

class LoadingScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.overrideredirect(True)
        self.geometry('300x200')
        self.configure(bg='white')
        self.center_window()

        # Load and display the GIF
        current_dir = os.path.dirname(__file__)
        self.gif_path = os.path.join(current_dir, 'loading.gif')
        self.gif = Image.open(self.gif_path)
        self.frames = []
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(self.gif.copy()))
                self.gif.seek(len(self.frames))
        except EOFError:
            pass

        self.label = tk.Label(self, bg='white')
        self.label.pack(expand=True, fill='both')

        self.current_frame = 0
        self.animate()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def animate(self):
        self.label.configure(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(50, self.animate)