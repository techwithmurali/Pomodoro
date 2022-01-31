from tkinter import *
import math
from plyer import notification
from tkinter import messagebox
import winsound
import os

def beep():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 100  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

def _quit():
    window.quit()
    window.destroy()
    exit()

def text_notify(Message):
    notification.notify(
    title = "Notification Alert!!!!!",
    message  = Message,
    app_icon = 'images/tomato.ico', #image that appears next to tite and message
    timeout = 10)
    print('done with text notify')


def Notify(message):
    print('inside notify')
    beep()
    text_notify(message)

def get_breaktimings():
    print('inside get_breaktimings')
    if os.path.exists('config.txt'):
        with open('config.txt','r') as fp:
            lst_lines = fp.readlines()
        try:
            wrktime = int(lst_lines[0].split('WRKTIME:')[1])
            shortbreaktime = int(lst_lines[1].split('SHORTBREAKTIME:')[1])
            longbreaktime = int(lst_lines[2].split('LONGBREAKTIME:')[1])
        except:
            messagebox.showinfo("showinfo", " Could not retreive saved settings..Default setting will be applied..")
            wrktime = 25
            shortbreaktime = 5
            longbreaktime = 20
    else:
        wrktime = 25
        shortbreaktime = 5
        longbreaktime = 20
    print(f' Returning from  get_breaktimings : wrktime: {wrktime} shortbreaktime: {shortbreaktime} longbreaktime : {longbreaktime} ')
    return wrktime,shortbreaktime,longbreaktime

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
wrktime,shortbreaktime,longbreaktime = get_breaktimings()
WORK_MIN = wrktime #25
SHORT_BREAK_MIN = shortbreaktime #5
LONG_BREAK_MIN = longbreaktime #20
reps = 0
timer = None
g_reset = 0
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global g_reset
    g_reset = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    wrktime,shortbreaktime,longbreaktime = get_breaktimings()
    WORK_MIN = wrktime #25
    SHORT_BREAK_MIN = shortbreaktime #5
    LONG_BREAK_MIN = longbreaktime #20
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global g_reset
    wrktime,shortbreaktime,longbreaktime = get_breaktimings()
    WORK_MIN = wrktime #25
    SHORT_BREAK_MIN = shortbreaktime #5
    LONG_BREAK_MIN = longbreaktime #20    
    #print('g_reset is {}'.format(g_reset))
    if g_reset < 1 :
        g_reset = 1 
        global reps
        reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60
        # If it's the 1st/3rd/5th/7th rep
        if reps % 8 == 0:
            Message='Pomodoro Alert!!!! Please take a break for {} Minutes Right now!!!'.format(LONG_BREAK_MIN)
            Notify(Message)
            count_down(long_break_sec)
            title_label.config(text="Break", fg=RED)
        # If it's the 8th rep
        elif reps % 2 == 0:
            Message='Pomodoro Alert!!!! Please take a break for {} Minutes Right now!!!'.format(SHORT_BREAK_MIN)
            Notify(Message)
            count_down(short_break_sec)
            title_label.config(text="Break", fg=PINK)
        # If it's the 2nd/4th/6th rep
        else:
            Message='Pomodoro Alert!!!! Work Period Begins for next {} Minutes !!'.format(WORK_MIN)
            Notify(Message)
            count_down(work_sec)
            title_label.config(text="Work", fg=GREEN)

def fn_topSave():
    global txt_WrkTime
    global txt_ShortBreak
    global txt_LongBreak
    try:
        wrktime        = int(txt_WrkTime.get())
        shortbreaktime =  int(txt_ShortBreak.get())
        longbreaktime  =  int(txt_LongBreak.get())
    except ValueError:
        print('incorrect input... ')
    print(f'{wrktime} {shortbreaktime} {longbreaktime} ')
    with open('config.txt','w') as fp:
        fp.write(f'WRKTIME:{wrktime}'+ '\n')
        fp.write(f'SHORTBREAKTIME:{shortbreaktime}'+ '\n')
        fp.write(f'LONGBREAKTIME:{longbreaktime}'+ '\n')
    messagebox.showinfo("showinfo", "Settings Saved Successfully")
    global top
    top.destroy()
     

def fn_ResetDefaults():
    os.remove('config.txt')
    global top
    top.destroy()



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    global g_reset
    global reps
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        #Message = "Pomodoro Alert!!!!!  Time Up!!!!!"
        #Notify(Message)
        g_reset = 0
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        check_marks.config(text=marks)

def fnSettings():
    global top
    top = Toplevel()
    top.title("Pomodoro - Settings")
    top.iconbitmap('images/pomo_short.ico')
    top.config(padx=100, pady=50, bg='gray',borderwidth=2)
    frame_header = Frame(top)
    frame_header.config(relief = RIDGE,bg='gray',pady=0)
    frame_header.pack()

    frame_body = Frame(top)
    frame_body.config(relief = RIDGE,bg='gray')
    frame_body.pack()

    global txt_WrkTime
    global txt_ShortBreak
    global txt_LongBreak

    intvar_wrkTime = IntVar()
    intvar_ShortBreak = IntVar()
    intvar_LongBreak = IntVar()
    l_wrktime,l_shortbreaktime,l_longbreaktime = get_breaktimings()
 
    
    lblSetting  = Label(frame_header,text=" Pomodoro - Timing Settings",bg='gray',justify = CENTER, borderwidth=0, highlightthickness=0,font='Helvetica 18 bold')
    lblSetting.grid(column=1, row=1,pady=10)
    lblWrkTime = Label(frame_body,text="WorkTime",font = "Helvetica",borderwidth=0, highlightthickness=0, bg='gray',  relief="groove",width = 20)
    lblWrkTime.grid(column=0,   row=3,pady=10)
    txt_WrkTime = Entry(frame_body,width = 5,bg='gray',textvariable = intvar_wrkTime )
    intvar_wrkTime.set(l_wrktime)
    txt_WrkTime.grid(column=2, row=3,pady=10)
    
    lblShortBreak = Label(frame_body,text="Short Break Time",font = "Helvetica",borderwidth=0, highlightthickness=0,bg='gray',  relief="groove",width = 20)
    lblShortBreak.grid(column=0,   row=5,pady=10)
    txt_ShortBreak  = Entry(frame_body,width = 5,bg='gray', textvariable = intvar_ShortBreak)
    intvar_ShortBreak.set(l_shortbreaktime)
    txt_ShortBreak .grid(column=2, row=5,pady=10)

    lblLongBreak = Label(frame_body,text="Long Break Time",font = "Helvetica",borderwidth=0, highlightthickness=0,bg='gray',  relief="groove",width =20)
    lblLongBreak.grid(column=0,   row=7,pady=10)
    txt_LongBreak = Entry(frame_body,width = 5,bg='gray' , textvariable = intvar_LongBreak)
    intvar_LongBreak.set(l_longbreaktime)
    txt_LongBreak.grid(column=2, row=7,pady=10)
    
    frame_buttons = Frame(top)
    frame_buttons.config(relief = RIDGE,bg='gray' ,pady=10)
    frame_buttons.pack()

    btn = Button(frame_buttons,text = "Reset",font = "Helvetica",bg='gray', borderwidth=2, highlightthickness=1,command=fn_ResetDefaults,width = 8).grid(column=1, row=0,padx=20,pady=20)
    btn = Button(frame_buttons,text = "Save",font = "Helvetica",bg='gray', borderwidth=2, highlightthickness=1,command=fn_topSave,width = 8).grid(column=3, row=0,padx=20,pady=20)
    btn = Button(frame_buttons,text = "Close",font = "Helvetica",bg='gray',borderwidth=2, highlightthickness=1, command=top.destroy,width = 8).grid(column=5, row=0,padx=20,pady=20)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
#window.iconbitmap('images/pomo_short.ico')
window.config(padx=100, pady=50, bg=YELLOW)
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)
# Need to check the background colour of the canvas as well
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# highlightthicknes is used for making the highlight disappear
tomato_img = PhotoImage(file="images/tomato.png")
start_btn_img = PhotoImage(file='images/play50.png')
Reset_btn_img = PhotoImage(file='images/Reset.png')
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)
# count_down(5)
# x and y values are half of the width and the height
start_button = Button(text="Start",image =start_btn_img ,borderwidth=0, highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset",image =Reset_btn_img ,borderwidth=0, highlightthickness=0, command = reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(text="", fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

menubar = Menu()
window.config(menu = menubar)
settings_menu = Menu(menubar,tearoff = 0)
settings_menu.add_command(label="Settings",command = fnSettings)
settings_menu.add_separator()
settings_menu.add_command(label = "Exit",command = _quit)
menubar.add_cascade(label="Options",menu = settings_menu)

window.mainloop()
