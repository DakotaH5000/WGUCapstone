import os
import sys
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from DataModifiers.encoders import gender_encoder, Stress_Encoder ,SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder

def run_MentalHealth_model(*args, **kwargs):

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

# Use the function to load your CSV file
    csv_file_path = resource_path('trainingData/mental_health_and_technology_usage_2024.csv')

# Now use pandas to read the CSV
    df = pd.read_csv(csv_file_path)
    # Load the CSV file into a DataFrame
    #df = pd.read_csv('WGUCapstone/trainingData/mental_health_and_technology_usage_2024.csv')

    le = LabelEncoder()


    ##MOdify data
    df[df.columns[2]] = gender_encoder.fit_transform(df[df.columns[2]])  # Gender
    df[df.columns[7]] = MentalHealth_Encoder.fit_transform(df[df.columns[7]])
    df[df.columns[8]] = Stress_Encoder.fit_transform(df[df.columns[8]])
    df[df.columns[11]] = SupportSystem_encoder.fit_transform(df[df.columns[11]])
    df[df.columns[12]] = WorkEnviorment_Encoder.fit_transform(df[df.columns[12]])
    df[df.columns[13]] = OnlineSupport_encoder.fit_transform(df[df.columns[13]])
    df = df.drop(df.columns[0], axis=1)

    X = df.drop(df.columns[6], axis=1)
    y = df.iloc[:, 6]

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier
    rf = RandomForestClassifier(
        n_estimators=50,      
        max_depth=8,          
        min_samples_split=8,   
        min_samples_leaf=3,     
        class_weight=None,      
        random_state=42         
    )

    

    # Train the model
    rf.fit(X_train, y_train)

    # Make predictions matrix based off training data
    y_pred = rf.predict(X_test)
    #Get models output accuracy score
    accuracy = accuracy_score(y_test, y_pred)


    #If some sort of user input, create a data frame with that data, otherwise you the default data set
    if args:
        new_data = pd.DataFrame([kwargs],
        columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 'Gaming_Hours', 
                                    'Screen_Time_Hours', 'Stress_Level', 'Sleep_Hours', 'Physical_Activity_Hours', 
                                    'Support_Systems_Access', 'Work_Environment_Impact', 'Online_Support_Usage'])
        new_data.astype('Int64')
    else:
        print('Running without kwargs')
        new_data = pd.DataFrame([[25, 1, 5, 2, 1, 6, 3, 7, 2, 1, 3, 0]], 
                            columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 'Gaming_Hours', 
                                    'Screen_Time_Hours', 'Stress_Level', 'Sleep_Hours', 'Physical_Activity_Hours', 
                                    'Support_Systems_Access', 'Work_Environment_Impact', 'Online_Support_Usage'])
    # Use the model to predict mental health status
    predicted_status = rf.predict(new_data)
    y = le.fit_transform(y)

    # Inverse transform the predicted label back to the original category
    predicted_status_label = le.inverse_transform(predicted_status)
    
    #Calculate importance for each attribute and dispaly to user
    importances = rf.feature_importances_
    Attribute = X.columns
    importance_df = pd.DataFrame({'Attribute': Attribute, 'Importance': importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    #Create and display bar graph to user
    fig = px.bar(importance_df, x='Attribute', y='Importance', title='Attribute Weight for Mental Health', labels={'Importance': 'Importance Score', 'Attribute': 'Attribute'})
    fig.show()

    #Create and display scatter plot to user
    predicitions = pd.DataFrame(y_test, y_pred)
    fig2 = px.scatter(predicitions, x='Actual', y='Predicted')
    fig2.add_shape(type='line', x0=predicitions['Actual'].min(), x1=predicitions['Actual'].max(), y0=predicitions['Actual'].min(), y1=predicitions['Actual'].max())
    result = predicted_status_label[0]
    fig2.show()
    #Return an array of data that will be used to create displays for the user
    return [result, accuracy]