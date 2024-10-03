#If user inputs manual parameters, ensure they are the correct data type/format
from tkinter import StringVar
from sklearn.preprocessing import LabelEncoder    
#from .encoders import gender_encoder, Stress_Encoder, SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder


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

def assign_Key_Value_Pairs(targetParameter, userInput):
    assigned_pairs = {}
    for key, index in keys_and_indices:
        if key is not targetParameter and index < len(userInput):
                assigned_pairs[key] = userInput[index]
    return assigned_pairs


def scrub_User_input(targetParameter, manualDataEntry):
    manualDataEntry = [item.strip() for item in manualDataEntry.split(',')]
    print(f'manualDataEntry split : {manualDataEntry}')
    userInput = assign_Key_Value_Pairs(targetParameter, manualDataEntry)
    for index, value in userInput.items():
        print(value)
        if type(value) == str:
            try:
                value = int(value)
                if index == "OnlineSupport":
                    scrubbedInput = OnlineSupport_encoder.transform([value])[0]
                    scrubbedInput = int(scrubbedInput)
                    userInput[index] = scrubbedInput
                if index == "Gender":
                    scrubbedInput = gender_encoder.transform([value])[0]
                    scrubbedInput = int(scrubbedInput)
                    userInput[index] = scrubbedInput
                if index == "SupportSystem":
                    scrubbedInput = SupportSystem_encoder.transform([value])[0]
                    scrubbedInput = int(scrubbedInput)
                    userInput[index] = scrubbedInput
                if index == "Stress":
                    scrubbedInput = Stress_Encoder.transform([value])[0]
                    scrubbedInput = int(scrubbedInput)
                    userInput[index] = scrubbedInput
                if index == "WorkEnvironment":
                    scrubbedInput = WorkEnviorment_Encoder.transform([value])[0]
                    scrubbedInput = int(scrubbedInput)
                    userInput[index] = scrubbedInput
                if index == "Mental Health Level":
                    scrubbedInput = MentalHealth_Encoder.transform([value])[0]
                    scrubbedInput = int(scrubbedInput)
                    userInput[index] = scrubbedInput
            except ValueError:
                continue
    print(f' userInput: {userInput}')
    return userInput
#Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], MentalHealth[7], 
#Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
#parameterList= ["Mental Health Level", "Technology Usage Hours", "Social Media Usage Hours", "Gaming Hours", "Screen Time Hours", "Sleep Hours", "Physical Activity Hours"]
##userInput = [25, 'Female', 3.12, 4.58, 2.25, 6.23, 'Excellent', 'Medium' , 7.98, 2, 'Yes', 'Neutral', 'Yes']



#print(scrub_User_input(parameterList[0], userInput))