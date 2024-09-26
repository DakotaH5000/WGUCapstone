import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from typing import Self
from mentalHealthModel import run_model as mentalHealthModel

root = Tk()
root.title("Mental Health Predictor")



def open_file_dialog():
    filename = filedialog.askopenfilename()
    return filename
def run_model():
    errmsg=StringVar()
    if checkBoxStatus.get():
        if scrub_User_input(selectedParameter.get()):
            mentalHealthModel()
    else:
        selectedTest = parameterList.index(selectedParameter.get())
        print(f'Selected test is {selectedTest}')
        match selectedTest:
            case  0: #Case matches position in Parameter list array, value being given to function matches position of value in csvfile row
                mentalHealthModel(7)
            case 1:
                mentalHealthModel(3)
            case 2:
                mentalHealthModel(4)
            case 3:
                mentalHealthModel(5)
            case 4:
                mentalHealthModel(6)
            case 5:
                mentalHealthModel(9)
            case 6:
                mentalHealthModel(10)
            case 7:
                mentalHealthModel()
            case _:
                errmsg.set(f'Unknown input option of {selectedTest} please choose a different option.')
                print(errmsg.get())

#If user inputs manual parameters, ensure they are the correct data type/format
def scrub_User_input(targetParameter, **manualDataEntry):
    selectedTest = targetParameter
    print(f'target param is {targetParameter}')
    errmsg = StringVar()
    errmsg.set("")
    userData = manualDataEntry
    if targetParameter == "Select":
        errmsg.set("Select a parameter to test")
        print(errmsg.get())
        return False
    
    return True

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Allow expansion of window
mainframe.rowconfigure(1, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(3, weight=1)





#Get CSV file from user
csvPick = ttk.Label(mainframe, text="Select a CSV file to analyze").grid(column=0, row=0 )
userFileButton = ttk.Button(mainframe, text='Choose a file', command=open_file_dialog).grid(column=1, row=0, padx=15)


#Allow the user to pick the Parameter to run the test with
userChoiceLabel = ttk.Label(mainframe, text="Which Parameter to test?").grid(column=0, row=1)
parameterList= ["Mental Health Level", "Technology Usage Hours", "Social Media Usage Hours", "Gaming Hours", "Screen Time Hours", "Default output of training", "Sleep Hours", "Physical Activity Hours"]
selectedParameter= StringVar()
selectedParameter.set("Select")
parameterChoice = ttk.Menubutton(mainframe, textvariable=selectedParameter)
parameterChoice.grid(column=1, row=1)

#Add options to the menu, handle the event of selecting an Option
menu = tk.Menu(parameterChoice, tearoff=0)
parameterChoice["menu"] = menu
for param in parameterList:
    menu.add_command(label=param, command=lambda p=param: selectedParameter.set(p))


userManualData = StringVar().set("")
manualDataEntryBox = ttk.Entry(mainframe, textvariable=userManualData).grid(column=1, row=2)
manualDataEntryLabel = ttk.Label(mainframe, text="Enter manual data, seperated by commas").grid(column=0, row=2)
checkBoxStatus = tk.BooleanVar(value=FALSE)
def printStatus():
    print(checkBoxStatus.get())
manualDataCheckBox = ttk.Checkbutton(mainframe, variable=checkBoxStatus, command=printStatus).grid(column=2, row=2)

runReportButton = ttk.Button(mainframe, text='Run Model', command=run_model).grid(column=3, row=3, sticky=E, padx=20, pady=20)

root.mainloop()