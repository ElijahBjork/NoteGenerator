"""
Author:  Elijah Bjork
Purpose: Defines the GraphicsManager class
"""

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image
try:
    import StartingPoints
    import UserImage
    import pixel
except:
    print("Please run this script in the PFNoteGenerator directory.")

#Create a window that let's a user select pixels from an image.
class GraphicsManager:
    """Holds an instance of tk.TK and defines methods for manipulating the screen."""
    
    def __init__(self):
        """Creates the initial window."""
        self.root = tk.Tk()
        self.root.title('PF Note Generator')
        self.root.iconbitmap("./small.ico")
        
        #Create object to hold all the starting points
        self.sp = StartingPoints.StartingPoints()

        #Create image for workshop
        self.marker_image = tk.PhotoImage(file='./marker.png')
        self.scanned_image = tk.PhotoImage(file='./scanned.png')
        self.user_img = UserImage.UserImage()
        
        #Create welcome screen
        self.welcome_lf = ttk.Frame(self.root)
        self.welcome_lf.grid(column=1, row=2, padx=30, pady=10)
        self.welcome_lf['borderwidth'] = 5
        self.welcome_lf['relief'] = 'groove'

        ttk.Label(
            self.welcome_lf, 
            text="Welcome to PF Note Generator. First, create a png file with a fun note for a friend or significant other. Make sure it has a pure white background. (rgb: 255, 255, 255 hex: #ffffff) Then, click on all of the points you want to pathfind from. Make sure you have one point for every isolated block of pixels. This program will scan your image using a pathfinding algorithm. Then, it will generate a python script that will draw your image on screen with a fun effect.",
            font=("Helvetica", 14), 
            justify= tk.LEFT, 
            padding=10,
            wraplength= 350).pack()

        ttk.Button(
            self.welcome_lf,
            text= "Choose file",
            command=self.present_select_pixel_screen,
            padding=7,
            width=27).pack()
    
    def clear_screen(self):
        """Clears everything on the current screen."""
        for c in [child for child in self.root.children.values()]: #may seen redundant, but python gets onery if we loop through .values() directly. Instead we make a list of all values in .values() and loop through the list.                
                c.destroy()

    def present_select_pixel_screen(self):
        """Replaces the initial screen with the main work screen."""
        if self.user_img.filename == '[NOT SET]':
            self.user_img.chooseImage()
        
        self.clear_screen()
        
        self.marker_i = 0 #used to name markers
        
        self.user_image_label = ttk.Label(
            self.root,
            image=self.user_img.image,
            borderwidth=0
        )

        for pt in self.sp.starting_points:
            self.add_marker(pt.x, pt.y)

        self.user_image_label.bind("<Button-1>", lambda event: self.add_marker(event.x, event.y))
        self.user_image_label.pack()
        
        image_width = self.user_img.image.width()
        
        self.instruction = ttk.Label(
            self.root,
            text="Click on each block of pixels. You can remove any marker by clicking on it. Click here when you are finished.",
            font= ("Helvetica", 14),
            wraplength=image_width
        )

        self.instruction.bind("<Button-1>", lambda event: self.scan_image())
        self.instruction.pack()
        
    def add_marker(self, x, y):
        """Adds a marker to the screen"""
        x = x - 3
        y = y - 3
        
        self.marker_i += 1
        marker = tk.Label(
            self.root,
            image=self.marker_image,
            borderwidth=0,
            name='marker' + str(self.marker_i))
        marker.bind(
            "<Button-1>", 
            lambda event: event.widget.destroy()) #When the marker is clicked, it deletes itself.
        marker.place(x = x, y = y)
        
    def scan_image(self):
        """Scans an image"""
        
        ttk.Label(
            self.root,
            font=("Helvetica", 14), 
            text="Searching for pixels! Each Marker will turn black as its section is completed."
        ).pack()

        self.sp.starting_points = []
        self.markers = iter(child for child in self.root.children.values() if str(child)[1:7] == 'marker') #creates an iterator for the markers on screen
        self.all_points = []
        self.forms = [] # A list containing all the pixels in the order they should be displayed on screen
        try:
            self.picture = Image.open(self.user_img.filename)
        except:
            showinfo('Error', 'File moved or missing. Please restore or select a new file.')
            return
 
        self.root.after(1, self.scan_form)

    def scan_form(self):
        """Scans a form, then makes a call to scan the next form"""
        
        try: #get the next marker to pathfind from
            marker = next(self.markers)
            
        except: #if there are no more markers, destroy all elements presented on screen.
            self.clear_screen()
                
            self.picture_size = {'w': self.picture.size[0], 'h': self.picture.size[1]}
            self.picture.close()
            self.present()
            return
        
        x, y = marker.winfo_x() + 3, marker.winfo_y() + 3
        self.sp.add_point(x, y)

        pt = self.sp.starting_points[-1] #set the point to start from

        if (pt.asTuple()) in self.all_points: #check if this starting point is already in a form. If so, continue.
            marker.configure(image=self.scanned_image)
            self.root.after(1, self.scan_form)
            return
                
            
        form = [pixel.pixel(pt=pt.asTuple(), rgb=self.picture.getpixel(pt.asTuple()))]  # form is a list of pixels, beginning with a starting point. The program algorithmically adds pixels to this list until all adjacent non-white pixels are added.
        i = 0
        # pathfinding algorithm to find all adjacent non_white pixels
        while(i < len(form)):  # while loop iterates through an expanding list
            # get the adjecent points.
            cp =  [form[i].x, form[i].y]
            u_point = (cp[0], cp[1] - 1) #up
            d_point = (cp[0], cp[1] + 1) #down
            l_point = (cp[0] - 1, cp[1]) #left
            r_point = (cp[0] + 1, cp[1]) #right

            # generate list of points to avoid duplicate points
            points = [pixel.get_pt() for pixel in form]

            # if any point is not white, add it to the list. Ensure point is not in the list before adding it.
            u_pixel = pixel.pixel(pt=u_point, rgb=self.picture.getpixel(u_point))
            d_pixel = pixel.pixel(pt=d_point, rgb=self.picture.getpixel(d_point))
            l_pixel = pixel.pixel(pt=l_point, rgb=self.picture.getpixel(l_point))
            r_pixel = pixel.pixel(pt=r_point, rgb=self.picture.getpixel(r_point))

            if u_pixel.get_rgb() != [255, 255, 255] and u_point not in points:
                form.append(u_pixel)
                self.all_points.append((u_pixel.x, u_pixel.y))
            if d_pixel.get_rgb() != [255, 255, 255] and d_point not in points:
                form.append(d_pixel)
                self.all_points.append((d_pixel.x, d_pixel.y))
            if l_pixel.get_rgb() != [255, 255, 255] and l_point not in points:
                form.append(l_pixel)
                self.all_points.append((l_pixel.x, l_pixel.y))
            if r_pixel.get_rgb() != [255, 255, 255] and r_point not in points:
                form.append(r_pixel)
                self.all_points.append((r_pixel.x, r_pixel.y))

            i += 1

        self.forms.extend(form) #When the program finds all adjacent non-white pixels, the form is added to the list of pixels.

        marker.configure(image=self.scanned_image) #set the marker as scanned on screen
        
        self.root.after(1, self.scan_form) #call the next iteration
        

    def present(self):
        """Set's up the window to show the cool graphic. Also initiates the drawing of all pixels."""

        canvas = tk.Canvas(self.root, width=self.picture_size['w'], height=self.picture_size['h'], background='#ffffff')
        canvas.pack()

        #generated_i += 1
        self.generated_image = tk.PhotoImage(
            width=self.picture_size['w'], 
            height=self.picture_size['h'])

        canvas.create_image(self.picture_size['w'] / 2, self.picture_size['h'] / 2, image=self.generated_image)
        
        self.pixels = iter(self.forms)

        self.root.after(1, self.drawNextPixel)


    def drawNextPixel(self):
        """Every call retrieves the next pixel in the iterator and adds it to the screen. """
        try:
            p = next(self.pixels)
            self.generated_image.put(p.get_hex(), to=p.get_pt())
            self.root.after(1, self.drawNextPixel)
        except:
            ttk.Button(
                self.root,
                text="Save Script",
                command=self.saveFunNote
            ).pack() #Create Button to save script and end the program
            ttk.Button(
                self.root,
                text="Reselect Pixels",
                command=self.present_select_pixel_screen
            ).pack() #Create Button to go back to present_select_pixel_screen

    def saveFunNote(self):
        """Generates a python script that will open a tkinter window and display the fun graphic."""
        
        line1 = 'forms = ' + str([ {"hex": p["hex"], "x": p["x"], "y": p["y"]} for p in self.forms]).replace('\'', '"') #Create a list of objects with the pixel data in the order the pixels should be drawn onscreen.
        
        line2 = '\npicture_size = {"w": ' + str(self.picture_size['w']) + ', "h": ' + str(self.picture_size['h']) + '}' #Create a dictionary containing the height and width of the image.
        
        #This is essentially a copy of the present and drawNextPixel functions, as well as the code needed to create a tkinter window. This code takes the data recorded above and presents it on screen.
        line3_to_end = """ 

import tkinter as tk

#Create window
root = tk.Tk()
root.title('Note')
root.geometry(f'{picture_size["w"]}x{picture_size["h"]}')

#create image to draw pixels on
generated_image = tk.PhotoImage(name='generated_image', width=picture_size['w'], height=picture_size['h'])

pixels = iter(forms)
def drawNextPixel(): #Iterates through each pixel and draws it on screen.
    try:
        pixel = next(pixels)
    except:
        return
    generated_image.put(pixel['hex'], to=(pixel['x'], pixel['y']))
    root.after(1,drawNextPixel)

#Create Canvas to hold generated_image
canvas = tk.Canvas(root, width=picture_size['w'], height=picture_size['h'], background='#ffffff')
canvas.create_image(picture_size['w'] / 2, picture_size['h'] / 2, image=generated_image)
canvas.bind('<Visibility>', lambda event: drawNextPixel())
canvas.pack()

try: #windll helps tk not be blurry
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally: #Display the window
    root.mainloop()  

"""
        #Save the generated script to FunNote.py
        fun_note_file = open('./FunNote.py', 'w')
        fun_note_file.write(line1 + line2 + line3_to_end)
        fun_note_file.close()

        self.root.quit()



def main():

    g = GraphicsManager()


    try: #windll helps tk not be blurry
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally: #Display the window
        g.root.mainloop()

if __name__ == '__main__':
    main()