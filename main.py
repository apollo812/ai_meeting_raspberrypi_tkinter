# Import Module
from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
from tkinter import ttk
from app import start_recording, stop_recording, toggle_pause, createNewConnection, connect, get_wifi_status, set_content_length, get_meeting_list, delete_meeting_data, send_email
from datetime import datetime

#Setting state of meeting
Pause = False
is_paused = False
#Starter en timer som tjekker tiden
# Opret variabler til timeren
timer_running = False
MeetingLength = 0  # Længden på det aktuelle møde i sekunder
MeetingTotalLength = 0  # Samlet mødelængde i sekunder
timer_id = None  # Variabel til at holde id for timerhåndteringen
contentLength = "Short"
currentMeetingName = ""
currentMeetingIndex = 0
meetingList = []

MeetingLengthText = ""
PauseText = "Pause Mødet"

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

# Wifi connect modal
def open_connect_wifi_modal():
    modal = Toplevel(root)
    # Calculate the position to center the modal window
    parent_x = root.winfo_rootx()
    parent_y = root.winfo_rooty()
    parent_width = root.winfo_width()
    parent_height = root.winfo_height()

    modal_width = 205  # Set modal width
    modal_height = 100  # Set modal height

    x = parent_x + (parent_width - modal_width) // 2
    y = parent_y + (parent_height - modal_height) // 2
    modal.geometry(f"{modal_width}x{modal_height}+{x}+{y}")
    
    modal.title("Wifi")

    input1_label = Label(modal, text="SSID:")
    input1_entry = Entry(modal)
    input2_label = Label(modal, text="Password:")
    input2_entry = Entry(modal, show="*")
    ok_button = Button(modal, text="OK", command=lambda: handle_modal_input(input1_entry.get(), input2_entry.get(), modal))
    cancel_button = Button(modal, text="Cancel", command=modal.destroy)

    input1_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    input1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    input2_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    input2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    ok_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    cancel_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

def handle_modal_input(name, password, modal):
    # establish new connection
    createNewConnection(name, name, password)
    # connect to the wifi network
    connect(name, name)
    wifi_status = get_wifi_status()

    global wifi_image, nowifi_image
    if wifi_status:
        tab3_button_wifi['image'] = wifi_image
        modal.destroy()
    else:
        tab3_button_wifi['image'] = nowifi_image

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

def on_item_selected(event):
    global currentMeetingName, currentMeetingIndex
    selected_index = tab2_listbox.curselection()
    currentMeetingIndex = selected_index
    if selected_index:
        selected_item = tab2_listbox.get(selected_index[0])
        tab2_label_right["text"] = f"Meeting: {convert_time_format(selected_item)}"
        currentMeetingName = selected_item
        print(f"Item '{selected_item}' selected")

# Function to be called when a radio button is clicked
def on_radio_click():
    selected_option = radio_var.get()
    if selected_option == 1:
        set_content_length("Short")
    elif selected_option == 2:
        set_content_length("Medium")
    elif selected_option == 3:
        set_content_length("Long")

def clickDeleteMeeting():
    global meetingList, currentMeetingIndex
    delete_meeting_data(currentMeetingName)
    meetingList = get_meeting_list()

    tab2_listbox.delete(currentMeetingIndex)
    tab2_label_right["text"] = f"Meeting: {meetingList[0] if len(meetingList) > 0 else 'no data'}"

def clickSendEmail():
    global currentMeetingName
    print(currentMeetingName)
    email = entryEmail.get()
    send_email(currentMeetingName, email)

# tab 1
def clickRecord():
    global Pause, record_image, stop_image
    if Pause:
        tab1_button_recordstop['image'] = record_image

        audio_folder = "Audio_Recordings"
        stop_timer()
        stop_recording(audio_folder)
        Pause = False
    else:
        tab1_button_recordstop['image'] = stop_image
        tab1_button_playresume['image'] = resume_image

        start_timer()
        start_recording()
        Pause = True

def clickResumePlay():
    global is_paused, play_image, resume_image
    if is_paused:
        tab1_button_playresume['image'] = resume_image

        # Genoptag optagelsen
        resume_timer()
        toggle_pause()  # Brug toggle_pause for at genoptage
        is_paused = False
    else:
        tab1_button_playresume['image'] = play_image
        # Pause optagelsen
        pause_timer()
        toggle_pause()  # Brug toggle_pause for at pause
        is_paused = True

def start_timer():
    # Start timeren ved at planlægge første opdatering
    global timer_running
    timer_running = True
    update_timer()

def update_timer():
    global MeetingLength, timer_id
    if timer_running:
        MeetingLength += 1  # Tæl op med 1 sekund
        hours = MeetingLength // 3600
        minutes = (MeetingLength % 3600) // 60
        seconds = MeetingLength % 60
        time_string = f"Length {hours:02}:{minutes:02}:{seconds:02}"
        print(time_string)
        tab1_label["text"] = time_string
        timer_id = root.after(1000, update_timer)  # Planlæg næste opdatering om 1000 ms (1 sekund)

def pause_timer():
    # Pause timeren ved at stoppe de planlagte opdateringer, men uden at nulstille den akkumulerede tid
    global timer_running, timer_id
    timer_running = False
    if timer_id:
        root.after_cancel(timer_id)

def stop_timer():
    global timer_running, timer_id, MeetingLength, MeetingTotalLength
    # Stop timeren ved at annullere den planlagte opdatering
    timer_running = False
    if timer_id:
        root.after_cancel(timer_id)
    # Gem mødelængden og nulstil MeetingLength
    MeetingTotalLength += MeetingLength
    MeetingLength = 0

def resume_timer():
    global timer_running
    timer_running = True
    update_timer()  # Call the function to update the timer

def convert_time_format(input_string):
    # Parse input string into a datetime object
    dt = datetime.strptime(input_string, "%m-%d-%Y-%H-%M")

    # Format the datetime object into the desired format
    output_string = dt.strftime("%m-%d-%Y-%H:%M")
    return output_string

if __name__ == "__main__":
    # create root window
    root = Tk()
    root.geometry('586x330')
    root.title("CrossBox APP")

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
    logo_image = ImageTk.PhotoImage(Image.open("icon/logo.png").resize((100, 30)))
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
    record_image = ImageTk.PhotoImage(Image.open("icon/record.png").resize((140, 140)))
    stop_image = ImageTk.PhotoImage(Image.open("icon/stop.png").resize((140, 140)))
    
    tab1_button_recordstop = Button(tab1_button_frame, text="Button 1", image=record_image, bg=sub_frame_3.cget('bg'), relief=FLAT, command=lambda: clickRecord())
    tab1_button_recordstop.grid(row=0, column=0, ipadx=25)

    # load play button image
    playresume_image = ImageTk.PhotoImage(Image.open("icon/playresume.png").resize((140, 140)))
    play_image = ImageTk.PhotoImage(Image.open("icon/playbutton.png").resize((140, 140)))
    resume_image = ImageTk.PhotoImage(Image.open("icon/resumebutton.png").resize((140, 140)))

    tab1_button_playresume = Button(tab1_button_frame, text="Button 2", image=playresume_image, bg=sub_frame_3.cget('bg'), relief=FLAT, command=lambda: clickResumePlay())
    tab1_button_playresume.grid(row=0, column=1, ipadx=25)

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

    meetingList = get_meeting_list()

    # # Inserting some items into the listbox
    # items = ["26-11-2023-18:00", "26-11-2023-18:01", "26-11-2023-18:02", "26-11-2023-18:03", "26-11-2023-18:04",
    #         "26-11-2023-18:05", "26-11-2023-18:06", "26-11-2023-18:07", "26-11-2023-18:08", "26-11-2023-18:09",
    #         "26-11-2023-18:10", "26-11-2023-18:11", "26-11-2023-18:12", "26-11-2023-18:13", "26-11-2023-18:14",
    #         "26-11-2023-18:15", "26-11-2023-18:16", "26-11-2023-18:17", "26-11-2023-18:18", "26-11-2023-18:19",
    #         "26-11-2023-18:20", "26-11-2023-18:21", "26-11-2023-18:22", "26-11-2023-18:23", "26-11-2023-18:24",
    #         "26-11-2023-18:25", "26-11-2023-18:26", "26-11-2023-18:27", "26-11-2023-18:28", "26-11-2023-18:29"
    #         ]
    for item in meetingList:
        tab2_listbox.insert(END, item)

    currentMeetingName = meetingList[0] if len(meetingList) > 0 else "no data"

    # Apply color scheme to listbox items
    color_listbox_items(tab2_listbox)

    # Bind the click event to the listbox
    tab2_listbox.bind("<<ListboxSelect>>", on_item_selected)

    # Right layout - Label, Entry, and Button
    tab2_right_frame = Frame(tab_frames[2], width=436, height=280, bg="blue")
    tab2_right_frame.grid(row=0, column=1, sticky="n")
    
    tab2_label_right = Label(tab2_right_frame, text=f"Meeting: {currentMeetingName}", fg="white", font=tab1_length_font, bg=sub_frame_3.cget('bg'))
    tab2_label_right.place(relx=0.5, rely=0.15, anchor="center")

    tab2_input_frame = Frame(tab2_right_frame, bg=sub_frame_3.cget('bg'))
    tab2_input_frame.place(relx=0.5, rely=0.45, anchor="center")

    entryLabelFont = font.Font(family='OpenSans-Bold', weight="bold", size=18)

    entryEmail = Entry(tab2_input_frame, text="here", bg='#47535C', fg='#A1A7AA', font=entryLabelFont, width=25)
    entryEmail.grid(row=0, column=0)
    entryEmail.insert(0, 'Send summary to email...')


    # load play button image
    send_image = ImageTk.PhotoImage(Image.open("icon/send.png").resize((27, 27)))

    tab2_button_send = Button(tab2_input_frame, text="Button 2", image=send_image, bg="#36AFC8", relief=FLAT, command=clickSendEmail)
    tab2_button_send.grid(row=0, column=1)

    # load play button image
    trash_image = ImageTk.PhotoImage(Image.open("icon/trash.png").resize((50, 60)))

    button = Button(tab2_right_frame, text="Delete", image=trash_image, bg=sub_frame_3.cget('bg'), relief=FLAT, command=clickDeleteMeeting)
    button.place(relx=0.5, rely=0.85, anchor="center")


    # Third Tab
    tab3_left_frame = Frame(tab_frames[3], width=293, height=280, bg='blue')
    tab3_left_frame.grid(row=0, column=0, sticky="n")

    tab3_label_left = Label(tab3_left_frame, text="Connect to WIFI", fg="white", font=tab1_length_font, bg=sub_frame_3.cget('bg'))
    tab3_label_left.place(relx=0.5, rely=0.2, anchor="center")

    # wifi button
    wifi_status = get_wifi_status()
    wifi_image = ImageTk.PhotoImage(Image.open("icon/wifi.png").resize((340, 200)))
    nowifi_image = ImageTk.PhotoImage(Image.open("icon/nowifi.png").resize((340, 200)))

    if wifi_status:
        wifi_image_case = wifi_image
    else:
        wifi_image_case = nowifi_image
    tab3_button_wifi = Button(tab3_left_frame, text="Wifi", image=wifi_image_case, bg=sub_frame_3.cget('bg'), relief=FLAT, command=open_connect_wifi_modal)
    tab3_button_wifi.place(relx=0.5, rely=0.6, anchor="center")

    # Right layout
    tab3_summery_font = font.Font(family='OpenSans-Bold', weight="bold", size=15)
    tab3_radio_font = font.Font(family='OpenSans-Bold', weight="bold", size=13)

    tab3_right_frame = Frame(tab_frames[3], width=293, height=280, bg='blue')
    tab3_right_frame.grid(row=0, column=1, sticky="n")

    tab3_label_right = Label(tab3_right_frame, text="Length of summery", fg="white", font=tab3_summery_font, bg=sub_frame_3.cget('bg'))
    tab3_label_right.place(relx=0.5, rely=0.2, anchor="center")
    
    s = ttk.Style()
    s.configure('my.TRadiobutton', font=('OpenSans-Bold', 16), foreground='white', background='blue', indicatorsize=40)

    radio_var = IntVar()
    radio_var.set(1)
    radio1_tab3 = ttk.Radiobutton(tab3_right_frame, text="Short", variable=radio_var, value=1, width=15, style='my.TRadiobutton', command=on_radio_click)
    radio1_tab3.place(relx=0.5, rely=0.4, anchor="center")
    radio2_tab3 = ttk.Radiobutton(tab3_right_frame, text="Medium", variable=radio_var, value=2, width=15, style='my.TRadiobutton', command=on_radio_click)
    radio2_tab3.place(relx=0.5, rely=0.6, anchor="center")
    radio3_tab3 = ttk.Radiobutton(tab3_right_frame, text="Long", variable=radio_var, value=3, width=15, style='my.TRadiobutton', command=on_radio_click)
    radio3_tab3.place(relx=0.5, rely=0.8, anchor="center")

    # Show the first tab group contents on startup
    tab_frames[1].grid(row=1, column=0, sticky="nsew")

    root.mainloop()
