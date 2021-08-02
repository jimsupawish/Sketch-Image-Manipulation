# -*- coding: utf-8 -*-
"""
@author: jimsupawish
"""

"""
Some code applied from CodeAcademy Tkinter course (https://www.youtube.com/watch?v=YXPyB4XeYLA),
Tkinter documentation (https://tkdocs.com/), python documentations, and StackOverflow
"""

import tkinter
from tkinter import Tk, Label, filedialog, Checkbutton, Text, messagebox, Button, font
from image_manipulator import process_image

root = Tk()
root.title("Sketch  Image Manipulation")
baseFont = font.Font(family="Helvetica", name="base_font", size=20)
statusFont = font.Font(family="Helvetica", name="status_font", size=16)

descriptionLabel = Label(root, text="Welcome to Sketch Image Manipulation!", font=baseFont)
descriptionLabel.pack()

use_subplots = tkinter.IntVar(root)
use_edge_as_color = tkinter.IntVar(root)
dark_mode = tkinter.IntVar(root)
cartoon_effect = tkinter.IntVar(root)
save_enabled = tkinter.IntVar(root)

subplots_button = Checkbutton(root, text="Show comparison of the images", variable=use_subplots, font=baseFont)
subplots_button.pack()
color_edge_button = Checkbutton(root, text="Color the edges", variable=use_edge_as_color, font=baseFont)
color_edge_button.pack()
dark_mode_button = Checkbutton(root, text="Dark Mode (does not work with \"Color the edges\")", variable=dark_mode, font=baseFont)
dark_mode_button.pack()
cartoon_effect_button = Checkbutton(root, text="Cartoon Effect (experimental, does not work with \"Color the Edges\")", variable=cartoon_effect, font=baseFont)
cartoon_effect_button.pack()
save_enabled_button = Checkbutton(root, text="Automatically save the figure", variable=save_enabled, font=baseFont)
save_enabled_button.pack()

status_box = Text(root, state='disabled', height=5, width=50, font=statusFont)
status_box.pack()

def selectFile():
    filename = filedialog.askopenfilename()
    if (filename == None or filename == ""):
        return

    image_name = filename[max(0, filename.rfind("/") + 1):]
    status_box['state'] = 'normal'
    status_box.replace("1.0", "4.0", "Processing image " + image_name)
    status_box['state'] = 'disabled'
    process_image(filename, use_subplots.get(), use_edge_as_color.get(), dark_mode.get(), cartoon_effect.get(), save_enabled.get())
    status_box['state'] = 'normal'
    status_box.replace("2.0", "4.0", "\nProcessing done!\n")
    status_box['state'] = 'disabled'
    
selectFileButton = Button(root,text="Select Image File To Process",
                          command=selectFile, width=30, font=baseFont)
selectFileButton.pack()

# Close the program using the 'X' button from:
# https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
def handleClose():
    if messagebox.askokcancel(title="Quit", message="Do you want to quit the program?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", handleClose)
root.mainloop()

