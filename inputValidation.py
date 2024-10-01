#If user inputs manual parameters, ensure they are the correct data type/format
from tkinter import StringVar
from encoders import gender_encoder, Stress_Encoder ,SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder

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
        if key is not targetParameter:
            assigned_pairs[key] = userInput[index]
    return assigned_pairs


def scrub_User_input(targetParameter, manualDataEntry):
    userInput = assign_Key_Value_Pairs(parameterList[0], manualDataEntry)
    userInput = userInput
    print(userInput)
    for index, value in userInput.items():
        if type(index) == str:
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

    print(userInput)

    
    return True
#Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], MentalHealth[7], 
#Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
parameterList= ["Mental Health Level", "Technology Usage Hours", "Social Media Usage Hours", "Gaming Hours", "Screen Time Hours", "Sleep Hours", "Physical Activity Hours"]
userInput = [25, 'Female', 3.12, 4.58, 2.25, 6.23, 'Excellent', 'Medium' , 7.98, 2, 'Yes', 'Neutral', 'Yes']



print(scrub_User_input(parameterList[0], userInput))