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

def show_tab(tab_num):
    # Hide all tab frames
    for frame in tab_frames.values():
        frame.grid_forget()
    
    # Show the selected tab frame
    tab_frames[tab_num].grid(row=1, column=0, sticky="nsew")

def color_listbox_items(listbox):
    for index in range(listbox.size()):
        if index % 2 == 0:
            listbox.itemconfig(index, {'bg': '#575757'})
        else:
            listbox.itemconfig(index, {'bg': '#2C2C2C'})

def on_entry_click(event):
    if entry.get() == 'Enter your text here...':
        entry.delete(0, "end")
        entry.insert(0, '')
        entry.config(fg = 'black')

def on_focus_out(event):
    if entry.get() == '':
        entry.insert(0, 'Enter your text here...')
        entry.config(fg = 'grey')

if __name__ == "__main__":
    # create root window
    root = Tk()
    root.geometry('586x330')

    # Optional: Remove window decorations for a true full-screen experience
    # root.overrideredirect(True)
    root.resizable(width=False, height=False)

    # Main frame
    main_frame = Frame(root)
    main_frame.grid(row=0, column=0)

    # Sub frame 1
    sub_frame_1 = Frame(main_frame, width=586, height=50, bg='#2C2C2C')  # Assuming height 50 to mimic h-15
    sub_frame_1.grid(row=0, column=0)

    # Sub frame 2
    sub_frame_2 = Frame(sub_frame_1)
    sub_frame_2.grid(row=0, column=0)

    # Two col frames of sub frame 2
    # First col frame
    col_frame_1 = Frame(sub_frame_2, width=152, height=50, bg='#2C2C2C')  
    col_frame_1.grid(row=0, column=0, padx=(0, 1))

    # load logo image
    logo_image = ImageTk.PhotoImage(Image.open("logo.png").resize((100, 30)))
    Label(col_frame_1, width=147, height=46, image=logo_image, bg='#2C2C2C', highlightbackground='#2C2C2C', highlightcolor='#2C2C2C').pack(fill="both")

    # Second col frame
    col_frame_2 = Frame(sub_frame_2, width=436, height=50, bg='#2C2C2C')  
    col_frame_2.grid(row=0, column=1)

    # Create Font object for menu
    menuFont = font.Font(family='OpenSans-Bold', weight="bold", size=15)
    # Create null image for pixel adjustment of button
    null_image = PhotoImage(width=0, height=0)

    # Menu buttons
    # Meeting button
    button_meeting = Button(
        col_frame_2, 
        font=menuFont, 
        text="Meeting", 
        fg="white", 
        compound="center", 
        image=null_image, 
        width=137, 
        height=42, 
        bg=col_frame_2.cget('bg'), 
        relief=FLAT,
        command=lambda: show_tab(1)
    )
    button_meeting.grid(row=0, column=0)
    
    # Saved button
    button_saved = Button(
        col_frame_2, 
        font=menuFont, 
        text="Saved", 
        fg="white", 
        compound="center", 
        image=null_image, 
        width=137, 
        height=42, 
        bg=col_frame_2.cget('bg'), 
        relief=FLAT,
        command=lambda: show_tab(2)
    )
    button_saved.grid(row=0, column=1)

    # Settings button
    button_settings = Button(
        col_frame_2, 
        font=menuFont, 
        text="Settings", 
        fg="white", 
        compound="center", 
        image=null_image, 
        width=138, 
        height=42, 
        bg=col_frame_2.cget('bg'), 
        relief=FLAT,
        command=lambda: show_tab(3)
    )
    button_settings.grid(row=0, column=2)
    
    # Sub frame 3
    sub_frame_3 = Frame(main_frame, width=586, height=280, bg='blue')  
    sub_frame_3.grid(row=1, column=0, sticky="nsew")

    # Create tab frames
    tab_frames = {}
    for i in range(1, 4):
        tab_frames[i] = Frame(sub_frame_3, width=586, height=280, bg='blue')

    # Define the content for each tab frame

    # First Tab - Meeting
    # Create Font object for menu
    tab1_title_font = font.Font(family='OpenSans-Bold', weight="bold", size=23)
    tab1_length_font = font.Font(family='OpenSans-Bold', weight="bold", size=18)

    tab1_label = Label(tab_frames[1], text="Automatic meeting summary", fg="white", font=tab1_title_font, bg=sub_frame_3.cget('bg'))
    tab1_label.place(relx=0.5, rely=0.15, anchor="center")

    tab1_button_frame = Frame(tab_frames[1], bg=root.cget('bg'))
    tab1_button_frame.place(relx=0.5, rely=0.5, anchor="center")

    # load record button image
    record_image = ImageTk.PhotoImage(Image.open("record.png").resize((140, 140)))
    
    tab1_button_record = Button(tab1_button_frame, text="Button 1", image=record_image, bg=sub_frame_3.cget('bg'), relief=FLAT)
    tab1_button_record.grid(row=0, column=0, ipadx=25)

    # load play button image
    play_image = ImageTk.PhotoImage(Image.open("playbutton.png").resize((140, 140)))

    tab1_button_stop = Button(tab1_button_frame, text="Button 2", image=play_image, bg=sub_frame_3.cget('bg'), relief=FLAT)
    tab1_button_stop.grid(row=0, column=1, ipadx=25)

    tab1_label = Label(tab_frames[1], text="Length 00:00:00", fg="white", font=tab1_length_font, bg=sub_frame_3.cget('bg'))
    tab1_label.place(relx=0.5, rely=0.85, anchor="center")

    # Second Tab
    # Left layout - Listbox

    # Left layout - Label and Listbox
    listLabelFont = font.Font(family='OpenSans-Bold', weight="bold", size=12)

    tab2_left_frame = Frame(tab_frames[2], width=152, height=280)
    tab2_left_frame.grid(row=0, column=0, sticky="n")

    tab2_label_left = Label(tab2_left_frame, text="Meetings", font=listLabelFont, bg='#252525', fg='white')
    tab2_label_left.grid(row=0, column=0, sticky="nswe")

    tab2_listbox = Listbox(tab2_left_frame, width=25, bg='#2C2C2C', fg='white', relief='flat', highlightthickness=0, height=16)
    tab2_listbox.grid(row=1, column=0, sticky="n")

    # Inserting some items into the listbox
    items = ["26-11-2023-18:00", "26-11-2023-18:01", "26-11-2023-18:02", "26-11-2023-18:03", "26-11-2023-18:04",
            "26-11-2023-18:05", "26-11-2023-18:06", "26-11-2023-18:07", "26-11-2023-18:08", "26-11-2023-18:09",
            "26-11-2023-18:10", "26-11-2023-18:11", "26-11-2023-18:12", "26-11-2023-18:13", "26-11-2023-18:14",
            "26-11-2023-18:15", "26-11-2023-18:16", "26-11-2023-18:17", "26-11-2023-18:18", "26-11-2023-18:19",
            "26-11-2023-18:20", "26-11-2023-18:21", "26-11-2023-18:22", "26-11-2023-18:23", "26-11-2023-18:24",
            "26-11-2023-18:25", "26-11-2023-18:26", "26-11-2023-18:27", "26-11-2023-18:28", "26-11-2023-18:29"
            ]
    for item in items:
        tab2_listbox.insert(END, item)

    # Apply color scheme to listbox items
    color_listbox_items(tab2_listbox)

    # Right layout - Label, Entry, and Button
    tab2_right_frame = Frame(tab_frames[2], width=436, height=280, bg="blue")
    tab2_right_frame.grid(row=0, column=1, sticky="n")
    
    tab2_label_right = Label(tab2_right_frame, text="Meeting: 11-10-2023-11:20", fg="white", font=tab1_length_font, bg=sub_frame_3.cget('bg'))
    tab2_label_right.place(relx=0.5, rely=0.15, anchor="center")

    tab2_input_frame = Frame(tab2_right_frame, bg=sub_frame_3.cget('bg'))
    tab2_input_frame.place(relx=0.5, rely=0.45, anchor="center")

    entryLabelFont = font.Font(family='OpenSans-Bold', weight="bold", size=18)

    entry = Entry(tab2_input_frame, text="here", bg='#47535C', fg='#A1A7AA', font=entryLabelFont, width=25)
    entry.grid(row=0, column=0)
    entry.insert(0, 'Send summary to email...')


    # load play button image
    send_image = ImageTk.PhotoImage(Image.open("send.png").resize((27, 27)))

    tab1_button_stop = Button(tab2_input_frame, text="Button 2", image=send_image, bg="#36AFC8", relief=FLAT)
    tab1_button_stop.grid(row=0, column=1)

    # load play button image
    trash_image = ImageTk.PhotoImage(Image.open("trash.png").resize((50, 60)))

    button = Button(tab2_right_frame, text="Delete", image=trash_image, bg=sub_frame_3.cget('bg'), relief=FLAT)
    button.place(relx=0.5, rely=0.85, anchor="center")


    # Third Tab
    radio_var = StringVar()
    radio_var.set("Option 1")
    radio1_tab3 = Radiobutton(tab_frames[3], text="Option 1", variable=radio_var, value="Option 1")
    radio1_tab3.pack()
    radio2_tab3 = Radiobutton(tab_frames[3], text="Option 2", variable=radio_var, value="Option 2")
    radio2_tab3.pack()
    radio3_tab3 = Radiobutton(tab_frames[3], text="Option 3", variable=radio_var, value="Option 3")
    radio3_tab3.pack()
    label_tab3 = Label(tab_frames[3], text="Selected option: ")
    label_tab3.pack()

    # Show the first tab group contents on startup
    tab_frames[2].grid(row=1, column=0, sticky="nsew")

    root.mainloop()
