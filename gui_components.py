import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import webbrowser

def create_main_window(app):
    app.title("Mounting Solutions Finder")
    app.geometry("600x750")  # Increased window size to accommodate new elements

    # Load and resize the background image
    current_dir = os.path.dirname(__file__)
    bg_image = Image.open(os.path.join(current_dir, "background_logo.png"))
    bg_image = bg_image.resize((600, 750), Image.LANCZOS)
    app.bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a canvas and put the image on it
    app.canvas = tk.Canvas(app, width=600, height=750)
    app.canvas.pack(fill="both", expand=True)
    app.canvas.create_image(0, 0, image=app.bg_photo, anchor="nw")

    app.style = ttk.Style()
    app.style.theme_use('clam')
    app.style.configure('TLabel', font=('Arial', 11), background='SystemButtonFace')
    app.style.configure('TButton', font=('Arial', 11))
    app.style.configure('TCheckbutton', font=('Arial', 11), background='SystemButtonFace')

    main_frame = ttk.Frame(app.canvas, style='TFrame')
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    title_label = ttk.Label(main_frame, text="Mounting Solutions Finder", font=('Arial', 14, 'bold'))
    title_label.grid(column=0, row=0, columnspan=2, pady=(0, 10))

    # Wheelchair dropdown
    app.wheelchair_label = ttk.Label(main_frame, text="Select Wheelchair Model:")
    app.wheelchair_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=2)
    app.wheelchair_var = tk.StringVar()
    app.wheelchair_dropdown = ttk.Combobox(main_frame, textvariable=app.wheelchair_var, width=25)
    app.wheelchair_dropdown['values'] = [wc.model for wc in app.wheelchairs]
    app.wheelchair_dropdown.grid(column=1, row=1, padx=5, pady=2)

    # AAC Device dropdown
    app.device_label = ttk.Label(main_frame, text="Select AAC Device:")
    app.device_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=2)
    app.device_var = tk.StringVar()
    app.device_dropdown = ttk.Combobox(main_frame, textvariable=app.device_var, width=25)
    app.device_dropdown['values'] = [device.name for device in app.aac_devices]
    app.device_dropdown.grid(column=1, row=2, padx=5, pady=2)

    # Eyegaze checkbox
    app.eyegaze_var = tk.BooleanVar()
    app.eyegaze_checkbox = ttk.Checkbutton(main_frame, text="Using Eyegaze?", variable=app.eyegaze_var)
    app.eyegaze_checkbox.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

    # Submit button
    app.submit_button = ttk.Button(main_frame, text="Find Solutions", command=app.find_solutions)
    app.submit_button.grid(column=0, row=4, columnspan=2, padx=5, pady=5)

    # Caveat message
    app.caveat_text = tk.Text(main_frame, height=3, width=60, wrap=tk.WORD, font=('Arial', 10))
    app.caveat_text.grid(column=0, row=5, columnspan=2, padx=5, pady=5)
    app.caveat_text.insert(tk.END, "Below are solutions based on the information provided. "
                           "External case by case factors per chair may mean the suggested solution will not be suitable.")
    app.caveat_text.config(state=tk.DISABLED)

    # Recommended Solution label
    app.recommended_label = ttk.Label(main_frame, text="Recommended Solution:", font=('Arial', 11, 'bold'))
    app.recommended_label.grid(column=0, row=6, columnspan=2, sticky=tk.W, padx=5, pady=(10, 0))

    # Recommended Solution listbox
    app.recommended_listbox = tk.Listbox(main_frame, height=1, width=60, font=('Arial', 10))
    app.recommended_listbox.grid(column=0, row=7, columnspan=2, padx=5, pady=(0, 5))
    app.recommended_listbox.bind('<<ListboxSelect>>', app.on_solution_select)

    # Alternative Solutions label
    app.alternative_label = ttk.Label(main_frame, text="Alternative Solutions:", font=('Arial', 11, 'bold'))
    app.alternative_label.grid(column=0, row=8, columnspan=2, sticky=tk.W, padx=5, pady=(10, 0))

    # Alternative Solutions listbox
    app.alternative_listbox = tk.Listbox(main_frame, height=5, width=60, font=('Arial', 10))
    app.alternative_listbox.grid(column=0, row=9, columnspan=2, padx=5, pady=(0, 5))
    app.alternative_listbox.bind('<<ListboxSelect>>', app.on_solution_select)

    # Scrollbar for alternative solutions listbox
    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=app.alternative_listbox.yview)
    scrollbar.grid(column=2, row=9, sticky='ns')
    app.alternative_listbox['yscrollcommand'] = scrollbar.set

    # Result text
    app.result_text = tk.Text(main_frame, height=6, width=60, wrap=tk.WORD, font=('Arial', 10))
    app.result_text.grid(column=0, row=10, columnspan=2, padx=5, pady=5)
    app.result_text.tag_configure("hyperlink", foreground="blue", underline=1)
    app.result_text.bind("<Button-1>", lambda e: check_hyperlink(app, e))

    # Scrollbar for result text
    scrollbar_result = ttk.Scrollbar(main_frame, orient='vertical', command=app.result_text.yview)
    scrollbar_result.grid(column=2, row=10, sticky='ns')
    app.result_text['yscrollcommand'] = scrollbar_result.set

def check_hyperlink(app, event):
    index = app.result_text.index(f"@{event.x},{event.y}")
    tags = app.result_text.tag_names(index)
    if "hyperlink" in tags:
        url = app.result_text.get(index, f"{index} lineend")
        webbrowser.open_new(url.strip())