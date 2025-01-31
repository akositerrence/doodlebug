from tkinter import *

# SETUP
root = Tk()
root.title("DOODLEBUG V1")
root.geometry('500x500')

# GUI
def start_cycle():
    # PLACEHOLDER

start_button = Button(root, text = "▶", fg="black", command = start_cycle)
start_button.grid(0,0)



# EXECUTE 
root.mainloop()