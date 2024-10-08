import asyncio
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

#Import models
from DataModifiers.encoders import gender_encoder, Stress_Encoder ,SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder
from Models.mentalHealthModel import run_MentalHealth_model as mentalHealthModel
from Models.phyiscalActivityModel import run_physicalActivity_model as physicalActivityModel
from Models.techHoursModel import run_model as techHoursModel
from Models.socialMediaModel import run_model as socialMediaModel
from Models.gamingHoursModel import run_model as gamingHoursModel
from Models.screentimeModel import run_model as screenTimeModel
from Models.sleepHoursModel import run_model as sleepHoursModel
from DataModifiers.inputValidation import scrub_User_input


root = Tk()
root.title("Mental Health Predictor")



def open_file_dialog():
    filename = filedialog.askopenfilename()
    return filename

def run_async_task(async_func):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(async_func())
    else:
        loop.run_until_complete(async_func())

async def run_model():
    errmsg=StringVar()
    def show_error(msg):
        messagebox.showerror("Invalid input", msg)
    print(f'User input box is:{userManualData.get()}')
    if checkBoxStatus.get():
        selectedTest = parameterList.index(selectedParameter.get())
        scrubbedData = await scrub_User_input(selectedParameter.get(), userManualData.get())
        match selectedTest:
        
        #Upon testing each model was created into their own model to allow for tuning of the random forest in order to reduce overfitting of the parameters
            case  0: #Case matches position in Parameter list array, value being given to function matches position of value in csvfile row
                mentalHealthModel(scrubbedData)
            case 1:
                techHoursModel(scrubbedData)
            case 2:
                socialMediaModel(scrubbedData)
            case 3:
                gamingHoursModel([scrubbedData])
            case 4:
                screenTimeModel(scrubbedData)
            case 5:
                sleepHoursModel(scrubbedData)
            case 6:
                physicalActivityModel(scrubbedData)
            case None:
                errmsg.set(f'User Input in invalid format.')
                show_error(f'{errmsg.get()} at {scrubbedData[1]}')
            case _:
                errmsg.set(f'Unknown input option of {selectedTest} please choose a different option.')
                print(f'{errmsg.get()} at {scrubbedData[1]}')

    else:
        selectedTest = parameterList.index(selectedParameter.get())
        match selectedTest:

            #Upon testing each model was created into their own model to allow for tuning of the random forest in order to reduce overfitting of the parameters
            case  0: #Case matches position in Parameter list array, value being given to function matches position of value in csvfile row
                mentalHealthModel()
            case 1:
                techHoursModel()
            case 2:
                socialMediaModel()
            case 3:
                gamingHoursModel()
            case 4:
                screenTimeModel()
            case 5:
                sleepHoursModel()
            case 6:
                physicalActivityModel()
            case _:
                errmsg.set(f'Unknown input option of {selectedTest} please choose a different option.')
                print(errmsg.get())


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
selectedParameter= StringVar()
selectedParameter.set("Mental Health Level")
parameterList= ["Mental Health Level", "Technology Usage Hours", "Social Media Usage Hours", "Gaming Hours", "Screen Time Hours", "Sleep Hours", "Physical Activity Hours"]
parameterChoice = ttk.Menubutton(mainframe, textvariable=selectedParameter)
parameterChoice.grid(column=1, row=1)

#Add options to the menu, handle the event of selecting an Option
menu = tk.Menu(parameterChoice, tearoff=0)
parameterChoice["menu"] = menu
for param in parameterList:
    menu.add_command(label=param, command=lambda p=param: selectedParameter.set(p))


userManualData = StringVar()
manualDataEntryBox = ttk.Entry(mainframe, textvariable=userManualData)
manualDataEntryBox.grid(column=1, row=2)
manualDataEntryLabel = ttk.Label(mainframe, text="Enter manual data, seperated by commas").grid(column=0, row=2)
checkBoxStatus = tk.BooleanVar(value=FALSE)
def printStatus():
    print(checkBoxStatus.get())
manualDataCheckBox = ttk.Checkbutton(mainframe, variable=checkBoxStatus, command=printStatus).grid(column=2, row=2)

runReportButton = ttk.Button(mainframe, text='Run Model', command=lambda: run_async_task(run_model)).grid(column=3, row=3, sticky=E, padx=20, pady=20)

root.mainloop()

