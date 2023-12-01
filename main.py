# Import Module
from tkinter import *

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

if __name__ == "__main__":
    # create root window
    root = Tk()

    # root window title and dimension
    root.title("Automatic meeting summary")
    # root.config(bg="skyblue")
    # Set geometry (widthxheight)
    root.geometry('586x330')

    # Create Frame widget
    head_frame = Frame(root, width=586, height=50, bg='#2C2C2C')
    head_frame.grid(row=0, column=0, sticky="ew")

    
    main_frame = Frame(root, width=586, height=280, bg='blue')
    main_frame.grid(row=1, column=0, sticky="nsew")  # Add stickiness
    # main_frame.pack_propagate(False)  # Avoid automatic resizing of the main_frame
    # grad_main_frame = GradientFrame(main_frame, "#090863", "#1C1AD0", relief="flat")
    # grad_main_frame.place(relwidth=1, relheight=1)

    # all widgets will be here
    # Execute Tkinter
    root.mainloop()
