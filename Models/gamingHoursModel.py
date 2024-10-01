import csv
import threading
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from encoders import gender_encoder, Stress_Encoder ,SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder


#with open ('WGUCapstone/mental_health_and_technology_usage_2024.csv') as csvfile:
    #spamreader = csv.reader(csvfile, delimiter=',')
    #Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], MentalHealth[7], Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
    #for row in spamreader:
        #print(', '.join(row))


def run_model(**kwargs):
    # Load the CSV file into a DataFrame
    df = pd.read_csv('WGUCapstone/mental_health_and_technology_usage_2024.csv')

    # Debug printing


    le = LabelEncoder()


    ##MOdify data
    #Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], 
    #MentalHealth[7], Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
    df['Gender'] = gender_encoder.fit_transform(df['Gender'])  # Gender
    df['Mental_Health_Status'] = MentalHealth_Encoder.fit_transform(df['Mental_Health_Status'])
    df['Stress_Level'] = Stress_Encoder.fit_transform(df['Stress_Level'])
    df['Support_Systems_Access'] = SupportSystem_encoder.fit_transform(df['Support_Systems_Access'])
    df['Work_Environment_Impact'] = WorkEnviorment_Encoder.fit_transform(df['Work_Environment_Impact'])
    df['Online_Support_Usage'] = OnlineSupport_encoder.fit_transform(df['Online_Support_Usage'])
    df = df.drop(df.columns[0], axis=1)

    X = df.drop(df.columns[4], axis=1)  # All rows, all columns except the desired - 1
    y = df[df.columns[4]].astype(float)   # All rows, only the last desired column

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier
    rf = RandomForestRegressor(
        n_estimators=35,        # Number of trees in the forest
        max_depth=8,          # Maximum depth of the trees (None means nodes are expanded until all leaves are pure)
        min_samples_split=8,     # Minimum number of samples required to split an internal node
        min_samples_leaf=3,      # Minimum number of samples required to be at a leaf node
        random_state=42          # For reproducibility
    )

    # Train the model
    rf.fit(X_train, y_train)

    # Make predictions
    y_pred = rf.predict(X_test)

    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))


    # Define a new set of data (example data for a single individual)
    #Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], MentalHealth[7], Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
    # Define new data for prediction (make sure to match feature columns)
    new_data = pd.DataFrame([[22, 1, 5, 9, 1, 6, 3, 7, 2, 1, 3, 0]], 
                            columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 
                                    'Screen_Time_Hours', 'Mental_Health_Status', 'Stress_Level', 'Sleep_Hours', 
                                    'Physical_Activity_Hours', 'Support_Systems_Access', 
                                    'Work_Environment_Impact', 'Online_Support_Usage'])

    # Use the model to predict mental health status
    predicted_status = rf.predict(new_data)

    print(f'Predicted Gaming Hours: {predicted_status[0]}')