#Handle async function to allow model to run before returning
import asyncio
#csv importer used for when user attempts to load data from a csv
import csv
#Import tkinter files and tkinter library
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

#Import models and encoders
from DataModifiers.encoders import gender_encoder, Stress_Encoder ,SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder
from Models.mentalHealthModel import run_MentalHealth_model as mentalHealthModel
from Models.phyiscalActivityModel import run_physicalActivity_model as physicalActivityModel
from Models.techHoursModel import run_model as techHoursModel
from Models.socialMediaModel import run_model as socialMediaModel
from Models.gamingHoursModel import run_model as gamingHoursModel
from Models.screentimeModel import run_model as screenTimeModel
from Models.sleepHoursModel import run_model as sleepHoursModel
from DataModifiers.inputValidation import scrub_User_input

#Create main window and title the window
root = Tk()
root.title("Mental Health Predictor")

#Handle selected CSV by user, maintains inside the instance of the program
selectedFile = None

#Show results from any Regression model requested by the user
def show_regression_results(ps, mse, mae, rsqrd):
    resultsWindow = tk.Tk()
    resultsWindow.title("Regression Results")
    ttk.Label(resultsWindow, text=f"Predicted Status: {ps}").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(resultsWindow, text=f"MSE: {mse}").grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(resultsWindow, text=f"MAE: {mae}").grid(column=0, row=2, padx=10, pady=10)
    ttk.Label(resultsWindow, text=f"R-squared: {rsqrd}").grid(column=0, row=3, padx=10, pady=10)

#Show results from any classification model requested by the user
def show_classification_results(result, acc):
    resultsWindow = tk.Tk()
    resultsWindow.title("Classification Results")
    ttk.Label(resultsWindow, text=f"Predicted Mental Health Level: {result}").grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(resultsWindow, text=f"Model Accuracy with prediction: {acc}").grid(column=0, row=2, padx=10, pady=10)

#Handle opening file broswser allowing user to pick a csv file
def open_file_dialog():
    global selectedFile
    filename = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if filename:
        selectedFile = filename 

#Running sychronously results in the model not properly genearting the data required
def run_async_task(async_func):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(async_func())
    else:
        loop.run_until_complete(async_func())

#Determine which method the model is supposed to run on, run the desired model with desired settings
async def run_model():
    #Handle error messaging
    errmsg=StringVar()
    def show_error(msg):
        messagebox.showerror("Invalid input", msg)
    #Run if user input into textbox
    if checkBoxStatus.get():
        selectedTest = parameterList.index(selectedParameter.get())
        scrubbedData = await scrub_User_input(selectedParameter.get(), userManualData.get())
        match selectedTest:
        
        #Upon testing each model was created into their own model to allow for tuning of the random forest in order to reduce overfitting of the parameters
            case  0: #Case matches position in Parameter list array, value being given to function matches position of value in csvfile row
                result = mentalHealthModel(scrubbedData)
                show_classification_results(result[0], result[1])
            case 1:
                results = techHoursModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 2:
                results = socialMediaModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 3:
                results = gamingHoursModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 4:
                results = screenTimeModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 5:
                results = sleepHoursModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 6:
                results = physicalActivityModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case None:
                errmsg.set(f'User Input in invalid format.')
                show_error(f'{errmsg.get()} at {scrubbedData[1]}')
            case _:
                errmsg.set(f'Unknown input option of {selectedTest} please choose a different option.')
                print(f'{errmsg.get()} at {scrubbedData[1]}')
    #Run if user selected a CSV file
    elif csvCheckBox.get():
        print(f' user file is {selectedFile}')
        csvDATA= ""
        with open (selectedFile, encoding='utf-8-sig') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                csvDATA = ', '.join(row) 
                break
        print(csvDATA)
        selectedTest = parameterList.index(selectedParameter.get())
        scrubbedData = await scrub_User_input(selectedParameter.get(), userManualData.get())
        match selectedTest:
        
        #Upon testing each model was created into their own model to allow for tuning of the random forest in order to reduce overfitting of the parameters
            case  0: #Case matches position in Parameter list array, value being given to function matches position of value in csvfile row
                result = mentalHealthModel(scrubbedData)
                show_classification_results(result[0], result[1])
            case 1:
                results = techHoursModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 2:
                results = socialMediaModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 3:
                results = gamingHoursModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 4:
                results = screenTimeModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 5:
                results = sleepHoursModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case 6:
                results = physicalActivityModel(scrubbedData)
                show_regression_results(results[0], results[1], results[2], results[3])
            case None:
                errmsg.set(f'User Input in invalid format.')
                show_error(f'{errmsg.get()} at {scrubbedData[1]}')
            case _:
                errmsg.set(f'Unknown input option of {selectedTest} please choose a different option.')
                print(f'{errmsg.get()} at {scrubbedData[1]}')
    #Run default input
    else:
        selectedTest = parameterList.index(selectedParameter.get())
        scrubbedData = await scrub_User_input(selectedParameter.get(), userManualData.get())
        match selectedTest:

            #Upon testing each model was created into their own model to allow for tuning of the random forest in order to reduce overfitting of the parameters
            case  0: #Case matches position in Parameter list array, value being given to function matches position of value in csvfile row
                result = mentalHealthModel()
                show_classification_results(result[0], result[1])
            case 1:
                results = techHoursModel()
                show_regression_results(results[0], results[1], results[2], results[3])
            case 2:
                results = socialMediaModel()
                show_regression_results(results[0], results[1], results[2], results[3])
            case 3:
                results = gamingHoursModel()
                show_regression_results(results[0], results[1], results[2], results[3])
            case 4:
                results = screenTimeModel()
                show_regression_results(results[0], results[1], results[2], results[3])
            case 5:
                results = sleepHoursModel()
                show_regression_results(results[0], results[1], results[2], results[3])
            case 6:
                results = physicalActivityModel()
                show_regression_results(results[0], results[1], results[2], results[3])
            case _:
                errmsg.set(f'Unknown input option of {selectedTest} please choose a different option.')
                print(errmsg.get())

#Create primary window, declare and make it a grid
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
csvCheckBox = tk.BooleanVar(value=FALSE)
manualDataCheckBox = ttk.Checkbutton(mainframe, variable=csvCheckBox).grid(column=2, row=0)


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

#Create a text box to accept the users input for the data
userManualData = StringVar()
manualDataEntryBox = ttk.Entry(mainframe, textvariable=userManualData)
manualDataEntryBox.grid(column=1, row=2)
manualDataEntryLabel = ttk.Label(mainframe, text="Enter manual data, seperated by commas").grid(column=0, row=2)
checkBoxStatus = tk.BooleanVar(value=FALSE)
manualDataCheckBox = ttk.Checkbutton(mainframe, variable=checkBoxStatus).grid(column=2, row=2)

#Button to allow the user to initiate models running
runReportButton = ttk.Button(mainframe, text='Run Model', command=lambda: run_async_task(run_model)).grid(column=3, row=3, sticky=E, padx=20, pady=20)

#Part of tkinter boiler plate, stops function from auto completing and closing/not finishing launching
root.mainloop()

