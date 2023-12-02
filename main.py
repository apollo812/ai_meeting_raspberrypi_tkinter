# Import Module
from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk

class GradientFrame(Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="red", color2="black", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)
        self.bind("<Map>", self._draw_gradient)  # Handle window mapping events
 
    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        # self.lower("gradient")

def show_content(content_num):
    if content_num == 1:
        body_content.config(text="Content 1 displayed")
    elif content_num == 2:
        body_content.config(text="Content 2 displayed")
    elif content_num == 3:
        body_content.config(text="Content 3 displayed")

if __name__ == "__main__":
    # create root window
    root = Tk()
    root.geometry('586x330')

    # Optional: Remove window decorations for a true full-screen experience
    # root.overrideredirect(True)
    root.resizable(width=False, height=False)

    # Main frame with grid-row class
    main_frame = Frame(root)
    main_frame.grid(row=0, column=0)

    # Sub-frame with h-15 class
    sub_frame_1 = Frame(main_frame, width=586, height=50, bg='#2C2C2C')  # Assuming height 50 to mimic h-15
    sub_frame_1.grid(row=0, column=0)

    # Sub-frame within the h-15 frame with grid-col class
    sub_frame_2 = Frame(sub_frame_1)
    sub_frame_2.grid(row=0, column=0)

    # Two sub-frames within the grid-col class
    col_frame_1 = Frame(sub_frame_2, width=150, height=50, bg='#2C2C2C')  # Assuming width 50 to mimic col-span-1
    col_frame_1.grid(row=0, column=0, padx=(0, 1))

    # load image to be "edited"
    image = ImageTk.PhotoImage(Image.open("logo.png").resize((100, 30)))
    Label(col_frame_1, width=145, height=46, image=image, bg='#2C2C2C', highlightbackground='#2C2C2C', highlightcolor='#2C2C2C').pack(fill="both")

    col_frame_2 = Frame(sub_frame_2, width=436, height=50, bg='#2C2C2C')  # Assuming width 150 to mimic col-span-3
    col_frame_2.grid(row=0, column=1)

    # Create Font object
    myFont = font.Font(family='OpenSans-Bold', weight="bold", size=15)
    null_image = PhotoImage(width=0, height=0)

    button1 = Button(
        col_frame_2, 
        font=myFont, 
        text="Meeting", 
        fg="white", 
        compound="center", 
        image=null_image, 
        width=137, 
        height=42, 
        bg=col_frame_2.cget('bg'), 
        relief=FLAT,
        command=lambda: show_content(1)
    )
    button1.grid(row=0, column=0)
    
    button2 = Button(
        col_frame_2, 
        font=myFont, 
        text="Saved", 
        fg="white", 
        compound="center", 
        image=null_image, 
        width=137, 
        height=42, 
        bg=col_frame_2.cget('bg'), 
        relief=FLAT,
        command=lambda: show_content(2)
    )
    button2.grid(row=0, column=1)

    button3 = Button(
        col_frame_2, 
        font=myFont, 
        text="Settings", 
        fg="white", 
        compound="center", 
        image=null_image, 
        width=138, 
        height=42, 
        bg=col_frame_2.cget('bg'), 
        relief=FLAT,
        command=lambda: show_content(3)
    )
    button3.grid(row=0, column=2)
    
    # Sub-frame with h-60 class
    sub_frame_3 = Frame(main_frame, width=586, height=280, bg='blue')  # Assuming height 180 to mimic h-60
    sub_frame_3.grid(row=1, column=0)

    body_content = Label(sub_frame_3, text="Initial content")
    body_content.pack(pady=20)

    root.mainloop()
