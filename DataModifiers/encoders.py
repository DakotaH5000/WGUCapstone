from sklearn.preprocessing import LabelEncoder    

#Handle user inputs that are in the form of a string converting them to numpy. They will be converted to int64 elsewhere. 
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
