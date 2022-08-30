"""
Author:  Elijah Bjork
Purpose: Define the UserImage class
"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class UserImage():
    """Contains a string as a filename and a function to request a filename dialog. Dependent on tkinter."""
    
    def __init__(self, filename = '[NOT SET]'):
        self.filename = filename
        self.image = tk.PhotoImage()
        

    def chooseImage(self):
        self.filename = fd.askopenfilename(title="Choose your image", initialdir='./')

        try:
            self.image = tk.PhotoImage(file=self.filename)
        except:
            self.filename = '[NOT SET]'
            self.image = tk.PhotoImage()
            showinfo(title='Error', message= 'The selected file is not supported. Please select a .png.')