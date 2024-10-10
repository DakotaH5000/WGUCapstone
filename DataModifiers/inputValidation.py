#If user inputs manual parameters, ensure they are the correct data type/format
from tkinter import StringVar
from sklearn.preprocessing import LabelEncoder    
#from .encoders import gender_encoder, Stress_Encoder, SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder

#Issue arose when importing these models, moved into file during trouble shooting process, worked so wasn't a pressing issue currently.
#Gender Encoder
genders = ['Male', 'Female', 'Other']
gender_encoder = LabelEncoder()
gender_encoder.fit(genders)
#Mental Health Encoder
mentalHealthStatuses = ['Poor', 'Fair', 'Good', 'Excellent']
MentalHealth_Encoder = LabelEncoder()
MentalHealth_Encoder.fit(mentalHealthStatuses)
#Stress Encoder
stressLevels = ['Low', 'Medium', 'High']
Stress_Encoder = LabelEncoder()
Stress_Encoder.fit(stressLevels)
#SupportSystems
supportSystem = ['No', 'Yes']
SupportSystem_encoder = LabelEncoder()
SupportSystem_encoder.fit(supportSystem)
#WorkEnviorment
workEnviorment = ['Negative', 'Neutral', 'Positive']
WorkEnviorment_Encoder = LabelEncoder()
WorkEnviorment_Encoder.fit(workEnviorment)
#OnlineSUpport
onlineSupport = ['No', 'Yes']
OnlineSupport_encoder = LabelEncoder()
OnlineSupport_encoder.fit(onlineSupport)

#Used to assist in converting a user input into a dictionary to correlate inputs
keys_and_indices = [
    ("Age", 0),
    ("Gender", 1),
    ("Technology Usage Hours", 2),
    ("Social Media Usage Hours", 3),
    ("Gaming Hours", 4),
    ("Screen Time Hours", 5),
    ("Mental Health Level", 6),
    ("Stress", 7),
    ("Sleep Hours", 8),
    ("Physical Activity Hours", 9),
    ("SupportSystem", 10),
    ("WorkEnvironment", 11),
    ("OnlineSupport", 12)
]

#Assign keys_and_indices user values to allow for data transfomration
def assign_Key_Value_Pairs(targetParameter, userInput):
    assigned_pairs = {}
    for key, index in keys_and_indices:
        if key is not targetParameter and index < len(userInput):
                assigned_pairs[key] = userInput[index]
    return assigned_pairs

#If input is not a type int, attempt to encode it, to a standardized form int for the model to investigate.
async def scrub_User_input(targetParameter, manualDataEntry):
    manualDataEntry = [item.strip() for item in manualDataEntry.split(',')]
    userInput = assign_Key_Value_Pairs(targetParameter, manualDataEntry)
    for key, value in userInput.items():
        if isinstance(value, str):
            match key:
                case "OnlineSupport":
                    try: 
                        userInput[key] = OnlineSupport_encoder.transform([value])[0]
                    except:
                        continue
                case 'Gender':
                    try: 
                        userInput[key] = int(gender_encoder.transform([value])[0])
                    except:
                        userInput[key] = int(value)
                case "SupportSystem":
                    try:
                        userInput[key] = SupportSystem_encoder.transform([value])[0]
                    except:
                        userInput[key] = int(value)
                case "Stress":
                    try: 
                        userInput[key] = int(Stress_Encoder.transform([value])[0])
                    except:
                        continue
                case "WorkEnvironment":
                    try: 
                        userInput[key] = WorkEnviorment_Encoder.transform([value])[0]
                    except:
                        userInput[key] = int(value)
                case "Mental Health Level":
                    try: 
                        userInput[key] = MentalHealth_Encoder.transform([value])[0]
                    except:
                        userInput[key] = int(value)
                case _:
                        continue
        else:
            continue
    #Return user input in the form to be used future functions for analysis.
    return ', '.join(str(value) for value in userInput.values())
