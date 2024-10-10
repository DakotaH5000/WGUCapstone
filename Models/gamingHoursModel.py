import os
import sys
from numpy import float64
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from DataModifiers.encoders import gender_encoder, Stress_Encoder ,SupportSystem_encoder, OnlineSupport_encoder, WorkEnviorment_Encoder, MentalHealth_Encoder


def run_model(*args, **kwargs):
    
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
    
    
    #df = pd.read_csv('WGUCapstone/trainingData/mental_health_and_technology_usage_2024.csv')
    # Debug printing


    le = LabelEncoder()

    #Encoder imported from encoders file to match schema
    df['Gender'] = gender_encoder.fit_transform(df['Gender'])  # Gender
    df['Mental_Health_Status'] = MentalHealth_Encoder.fit_transform(df['Mental_Health_Status'])
    df['Stress_Level'] = Stress_Encoder.fit_transform(df['Stress_Level'])
    df['Support_Systems_Access'] = SupportSystem_encoder.fit_transform(df['Support_Systems_Access'])
    df['Work_Environment_Impact'] = WorkEnviorment_Encoder.fit_transform(df['Work_Environment_Impact'])
    df['Online_Support_Usage'] = OnlineSupport_encoder.fit_transform(df['Online_Support_Usage'])
    df = df.drop(df.columns[0], axis=1)
    #Remove x column to train on
    X = df.drop(df.columns[4], axis=1)  # All rows, all columns except the desired - 1
    y = df[df.columns[4]].astype(float)   # All rows, only the last desired column

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # Initialize the Random Forest Regressor, parameters tested to attempt to increase accuracy
    rf = RandomForestRegressor(
        n_estimators=100,        
        max_depth= 5,          
        min_samples_split=8,    
        min_samples_leaf=3,      
        random_state=42         
    )

    # Train the model
    rf.fit(X_train, y_train)

    # Make predictions
    y_pred = rf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rsqrd = r2_score(y_test, y_pred)


   #If user gave input create a data frame with it and convert to int 64, otherwiese use default dataFrame
    if args:
        new_data = pd.DataFrame([kwargs],
                                columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 
                                        'Screen_Time_Hours', 'Mental_Health_Status', 'Stress_Level', 'Sleep_Hours', 
                                        'Physical_Activity_Hours', 'Support_Systems_Access', 
                                        'Work_Environment_Impact', 'Online_Support_Usage'])
        new_data.astype('Int64')
    else:
        new_data = pd.DataFrame([[25, 1, 5, 9, 1, 6, 3, 7, 2, 1, 3, 0]], 
                                columns=['Age', 'Gender', 'Technology_Usage_Hours', 'Social_Media_Usage_Hours', 
                                        'Screen_Time_Hours', 'Mental_Health_Status', 'Stress_Level', 'Sleep_Hours', 
                                        'Physical_Activity_Hours', 'Support_Systems_Access', 
                                        'Work_Environment_Impact', 'Online_Support_Usage'])
        new_data.astype('Int64')

    #Generate prediction based off data that was determined. 
    predicted_status = rf.predict(new_data)

    #Return a bar graph to the user to show weighting of data
    importances = rf.feature_importances_
    Attribute = X.columns
    importance_df = pd.DataFrame({'Attribute': Attribute, 'Importance': importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    fig = px.bar(importance_df, x='Attribute', y='Importance', title='Attribute Weight for Gaming Hours', labels={'Importance': 'Importance Score', 'Attribute': 'Attribute'})
    fig.show()

    predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    #Return a scatter plot to show distriubtion of data
    fig2 = px.scatter(predictions_df, x='Actual', y='Predicted')
    fig2.add_shape(type='line', x0=predictions_df['Actual'].min(), x1=predictions_df['Actual'].max(), y0=predictions_df['Actual'].min(), y1=predictions_df['Actual'].max())
    fig2.show()
    #Return an array of data points to create a visualization for the user.
    return [predicted_status[0], mse, mae, rsqrd]