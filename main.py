import tkinter as tk
from loading_screen import LoadingScreen
from data_loader import load_data
from solution_finder import find_solutions, on_solution_select
from gui_components import create_main_window, check_hyperlink
import threading
import time
import webbrowser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.loading_screen = LoadingScreen(self)
        
        # Start loading data in a separate thread
        threading.Thread(target=self.load_data, daemon=True).start()

    def load_data(self):
        start_time = time.time()
        
        load_data(self)

        elapsed_time = time.time() - start_time
        remaining_time = max(0, 3 - elapsed_time)
        time.sleep(remaining_time)

        self.after(0, self.setup_main_window)

    def setup_main_window(self):
        create_main_window(self)
        self.loading_screen.destroy()
        self.deiconify()

    def find_solutions(self):
        find_solutions(self)

    def on_solution_select(self, event):
        on_solution_select(self, event)

if __name__ == "__main__":
    app = App()
    app.mainloop()