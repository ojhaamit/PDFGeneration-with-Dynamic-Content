from tkinter import *
import sqlite3
from tkinter import messagebox, filedialog
from subprocess import Popen
from ThirdPdf import g_letter

root = Tk()
root.title("Dynamic PDF Generator")
root.minsize(600, 400)
root.maxsize(600, 400)

# Create database connection
conn = sqlite3.connect("letters.db")
cursor = conn.cursor()

# Create table
cursor.execute("""CREATE TABLE IF NOT EXISTS lvariables(
    p_num number,
    f_name text,
    l_name text,
    f_add text,
    s_add text,
    city text,
    state text,
    zip_code number,
    country text,
    p_amount number )
""")

#Commit Changes
conn.commit()

#Close Connection
conn.close()

#Function for browsing file
def browse():
    #Browse File using filedialog
    filename=filedialog.askopenfilename()
    #insert file path into entry box
    entry.insert(0, filename)

#Function for adding data in database
def a_data():
    path = entry.get()
    if (path!=""):
        # Create database connection
        conn = sqlite3.connect("letters.db")
        cursor = conn.cursor()

        #Load Data in Table
        filename = entry.get()
        fdata=[]
        with open(filename, "r") as fname:
            next(fname)
            for line in fname:
                line = line.rstrip()
                line = line.split(",")
                fdata.append(line)
        conn.executemany("INSERT INTO lvariables VALUES (?,?,?,?,?,?,?,?,?,?)", fdata)

        print(fdata)
        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()

    else:
        messagebox.showinfo("Alert", "Please enter path!")

canvas = Canvas(root, height=400, width=600)
canvas.pack()

#Layout
frame = Frame(root, bd=2)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor = "n")

entry = Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

my_button1 = Button(frame, text = "Browse File", bg="gray", command = browse)
my_button1.place(relx=0.7, relheight= 1, relwidth=0.3)

lower_frame = Frame(root, bd=2)
lower_frame.place(relx = 0.50, rely = 0.5, relwidth = 0.75, relheight = 0.10, anchor="n")

my_button2 = Button(lower_frame, text = "Add Data", bg="gray", command = a_data)
my_button2.place(relwidth=0.30, relheight=1)

my_button3 = Button(lower_frame, text = "Generate Letter", bg="gray", command = g_letter)
my_button3.place(relx =0.70, relwidth=0.3, relheight=1)

root.mainloop()