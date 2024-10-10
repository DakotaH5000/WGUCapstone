import os
import sys
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, mean_squared_error, mean_absolute_error, r2_score
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
    
    le = LabelEncoder()


    ##MOdify data with encoders
    df['Gender'] = gender_encoder.fit_transform(df['Gender'])  # Gender
    df['Mental_Health_Status'] = MentalHealth_Encoder.fit_transform(df['Mental_Health_Status'])
    df['Stress_Level'] = Stress_Encoder.fit_transform(df['Stress_Level'])
    df['Support_Systems_Access'] = SupportSystem_encoder.fit_transform(df['Support_Systems_Access'])
    df['Work_Environment_Impact'] = WorkEnviorment_Encoder.fit_transform(df['Work_Environment_Impact'])
    df['Online_Support_Usage'] = OnlineSupport_encoder.fit_transform(df['Online_Support_Usage'])
    df = df.drop(df.columns[0], axis=1)

    #Drop column we wish to study
    X = df.drop(df.columns[3], axis=1)  
    y = df.iloc[:, 3]  

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Regressor
    rf = RandomForestRegressor(
    n_estimators=55,        
    max_depth=8,          
    min_samples_split=8,    
    min_samples_leaf=3,    
    random_state=42         
    )

    # Train the model
    rf.fit(X_train, y_train)

    # Make predictions using training
    y_pred = rf.predict(X_test)

    #If user input, create a data frame with it, else default input
    if args:
        new_data = pd.DataFrame([kwargs],
                                columns=['Age', 'Gender', 'Technology_Usage_Hours',  'Gaming_Hours', 
                                    'Screen_Time_Hours', 'Mental_Health_Status', 'Stress_Level', 'Sleep_Hours', 'Physical_Activity_Hours', 
                                    'Support_Systems_Access', 'Work_Environment_Impact', 'Online_Support_Usage'])
        new_data.astype('Int64')
    else:
        new_data = pd.DataFrame([[25, 1, 5, 2, 1, 6, 3, 7, 2, 1, 3, 0]], 
                            columns=['Age', 'Gender', 'Technology_Usage_Hours',  'Gaming_Hours', 
                                    'Screen_Time_Hours', 'Mental_Health_Status', 'Stress_Level', 'Sleep_Hours', 'Physical_Activity_Hours', 
                                    'Support_Systems_Access', 'Work_Environment_Impact', 'Online_Support_Usage'])
    # Use the model to predict social media usage time
    predicted_status = rf.predict(new_data)
    y = le.fit_transform(y)
    # Inverse transform the predicted label back to the original label

    y_pred = rf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rsqrd = r2_score(y_test, y_pred)

    #Create a predicted Status off training and input
    predicted_status = rf.predict(new_data)

    #Return a bar graph to the user to show weighting of data
    importances = rf.feature_importances_
    Attribute = X.columns
    importance_df = pd.DataFrame({'Attribute': Attribute, 'Importance': importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    fig = px.bar(importance_df, x='Attribute', y='Importance', title='Attribute Weight for Gaming Hours', labels={'Importance': 'Importance Score', 'Attribute': 'Attribute'})
    fig.show()

    predictions_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    #Return scatter plot
    fig2 = px.scatter(predictions_df, x='Actual', y='Predicted')
    fig2.add_shape(type='line', x0=predictions_df['Actual'].min(), x1=predictions_df['Actual'].max(), y0=predictions_df['Actual'].min(), y1=predictions_df['Actual'].max())
    fig2.show()

    return [predicted_status[0], mse, mae, rsqrd]