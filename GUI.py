from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import font
import tkinter as tk
import pyttsx3

# Neural Net OCR GUI (NOG)
# A small wrapper to allow the user to select the file for processing using
# a common file selection dialog box

from nocr import nocr


root = Tk()
def about_window():
    top = tk.Toplevel(bg='#CD5C5C')
    tk.Label(top, text= "About the PhotoTextToSpeech Program:\n"
                       "This program will convert a screenshot of text in a word document into\n"
                       "text a computer can understand and to have this program say what is written.\n"
                       "As of right now, you can only make this work with one line of text from a\n"
                       "snippet image of a word document.").pack(padx=50, pady=50)

    top.mainloop()
    top.quit()

def how_window():
    top = tk.Toplevel(bg='#3DC9C5')
    tk.Label(top, text="How the PhotoTextToSpeech Program Works:\n"
                       "To use this program, simply start by clicking the browse button\n"
                       "The program can only find .png image files. File Explorer will not look for any other file types\n"
                       "Once you find the image you want, double click the image\n"
                       "The image file path will be sent to the file path entry text box\n"
                       "Once you see the image file path, Click GO\n"
                       "The program will try to work out what the image of text is and respond to you with what\n"
                       "the image says").pack(padx=50, pady=50)
    top.mainloop()
    top.quit()

# Opens file explorer to find an image for user
def browse_button():
    root.filename = filedialog.askopenfilename(parent=root, title='Select an Image', initialdir='/',
    filetypes=[('png files','*.png')])
    entry1.configure(state=NORMAL)
    entry1.delete(0, "end")
    entry1.insert(0, root.filename)
    entry1.configure(state=DISABLED)
    print("user selected file: ", root.filename)

def go_button():
    print("go pressed")
    text_found = nocr(root.filename)
    canvas1.delete(root.goText)
    root.goText = canvas1.create_text((250, 320), text=text_found, font="MSGothic 12 bold",
                        fill="#FFFFFF")
    print("guiOCR read: ", text_found)
    root.engine.say(text_found)
    root.engine.runAndWait()




# Opens about window or instructions window
# def hello():
#     print("hello!")

menubar = Menu(root)

# create a help and quit pulldown menu, and add it to the menu bar
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About this program", command=about_window)
helpmenu.add_command(label="How to use program", command=how_window)
menubar.add_cascade(label="Help", menu=helpmenu)

menubar.add_cascade(label="Exit",command=root.quit)
# display the menu
root.config(menu=menubar)

root.title("PhotoTextToSpeech")
root.resizable(0,0)
fileText = StringVar(None)
buttonBackgroundFont = font.Font(family='Helvetica', size=12, weight='bold')

canvas1 = Canvas(root, width=500, height=400)

backgroundImage=ImageTk.PhotoImage(Image.open("gui_resources/blueBackground2.jpg"))
root.iconbitmap("gui_resources/iconChat3.ico")

canvas1.create_image(0,0, anchor=NW, image=backgroundImage)
canvas1.pack()

entry1 = Entry(root)
canvas1.create_window(200, 140, width=300, height=25, window=entry1)

# Go button to run the program
goButton = Button(text="GO", font = buttonBackgroundFont, bd = 4,
                  bg='#00FF00', fg="#006400", padx=20, pady=10, command=go_button)
goButton.place(relx=0.4, rely=0.43)

# Exits out of the program
quitButton = Button(text="QUIT", font = buttonBackgroundFont, bd = 4,
                    bg='#000000', fg="#FFFFFF", padx=20, pady=10, command=root.quit)
quitButton.place(relx=0.38, rely=0.83)

# Browses for a specific file
browseButton = Button(root,  text="Browse...", padx=10, pady=5, command=browse_button)
browseButton.place(relx=.80, rely=.31)

# text read from image
#imageTextFinaL = canvas1.create_text((250, 320), text="This is where the text that is read will go.", font="MSGothic 12 bold", fill="#FFFFFF")
# go button description
root.goText = canvas1.create_text((125, 200), text="Convert to speech:", font="MSGothic 12 bold", fill="#FFFFFF")
# browse file description
searchFileText = canvas1.create_text((165, 120), text="Search for an image to be read:", font="MSGothic 12 bold", fill="#FFFFFF")

# init tts engine
root.engine = pyttsx3.init()
root.engine.setProperty('rate', 150)
root.engine.setProperty('volume', 1.0)
# voices = root.engine.getProperty('voices')
# root.engine.setProperty('voice', voices[1].id)
root.filename = ""

root.mainloop()