from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from typing import Self
from mentalhealthpredict import run_model as mentalHealthModel

root = Tk()
root.title("Mental Health Predictor")



def open_file_dialog():
    filename = filedialog.askopenfilename()
    return filename
def run_model():
    mentalHealthModel()


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.pack()



#Get CSV file from user
csvPick = ttk.Label(mainframe, text="Select a CSV file to analyze").grid(column=1, row=1, sticky=W )

userFileButton = ttk.Button(mainframe, text='Choose a file', command=open_file_dialog).grid(column=2, row=1)

runReportButton = ttk.Button(mainframe, text='Run Model', command=run_model).grid(column=3, row=3)

root.mainloop()