import csv
import threading
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score


#with open ('WGUCapstone/mental_health_and_technology_usage_2024.csv') as csvfile:
    #spamreader = csv.reader(csvfile, delimiter=',')
    #Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], MentalHealth[7], Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
    #for row in spamreader:
        #print(', '.join(row))


def run_MentalHealth_model(*args, **kwargs):
    # Load the CSV file into a DataFrame
    df = pd.read_csv('WGUCapstone/mental_health_and_technology_usage_2024.csv')

    # Debug printing


    le = LabelEncoder()
    gender_encoder = LabelEncoder()
    MentalHealth_Encoder = LabelEncoder()
    Stress_Encoder = LabelEncoder()
    SupportSystem_encoder = LabelEncoder()
    WorkEnviorment_Encoder = LabelEncoder()
    OnlineSupport_encoder = LabelEncoder()

    ##MOdify data
    df[df.columns[2]] = gender_encoder.fit_transform(df[df.columns[2]])  # Gender
    df[df.columns[7]] = MentalHealth_Encoder.fit_transform(df[df.columns[7]])
    df[df.columns[8]] = Stress_Encoder.fit_transform(df[df.columns[8]])
    df[df.columns[11]] = SupportSystem_encoder.fit_transform(df[df.columns[11]])
    df[df.columns[12]] = WorkEnviorment_Encoder.fit_transform(df[df.columns[12]])
    df[df.columns[13]] = OnlineSupport_encoder.fit_transform(df[df.columns[13]])
    df = df.drop(df.columns[0], axis=1)

    X = df.drop(df.columns[6], axis=1)  # All rows, all columns except the desired - 1
    y = df.iloc[:, 6]   # All rows, only the last column

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=35,        # Number of trees in the forest
        max_depth=8,          # Maximum depth of the trees (None means nodes are expanded until all leaves are pure)
        min_samples_split=8,     # Minimum number of samples required to split an internal node
        min_samples_leaf=3,      # Minimum number of samples required to be at a leaf node
        class_weight=None,       # Weights associated with classes (use 'balanced' for class imbalance)
        random_state=42          # For reproducibility
    )

    # Train the model
    rf.fit(X_train, y_train)

    # Make predictions
    y_pred = rf.predict(X_test)

    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))


    # Define a new set of data (example data for a single individual)
    #Rows: uID[0], Age[1], Gender[2], TechHours[3], SocialHours[4], GamingHours[5], Screentime[6], MentalHealth[7], Stress[8], Sleephours[9], Physical activity[10], SupportSystem[11], WorkEnviorment[12], Online SUpport[13]
    if args:
        print('Running with kwargs')
        new_data = pd.DataFrame([kwargs],
        columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 'Gaming_Hours', 
                                    'Screen_Time_Hours', 'Stress_Level', 'Sleep_Hours', 'Physical_Activity_Hours', 
                                    'Support_Systems_Access', 'Work_Environment_Impact', 'Online_Support_Usage'])
    else:
        print('Running without kwargs')
        new_data = pd.DataFrame([[25, 1, 5, 2, 1, 6, 3, 7, 2, 1, 3, 0]], 
                            columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 'Gaming_Hours', 
                                    'Screen_Time_Hours', 'Stress_Level', 'Sleep_Hours', 'Physical_Activity_Hours', 
                                    'Support_Systems_Access', 'Work_Environment_Impact', 'Online_Support_Usage'])
    # Use the model to predict mental health status
    predicted_status = rf.predict(new_data)
    y = le.fit_transform(y)
    # Inverse transform the predicted label back to the original category (if LabelEncoder was used)
    predicted_status_label = le.inverse_transform(predicted_status)

    print(f'Predicted Mental Health Status: {predicted_status_label[0]}')