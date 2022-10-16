import streamlit as st
import pandas as pd
import numpy as np
import gdown
import plotly.express as px   # Use of plotly Graph 
import boto3
s3 = boto3.client('s3')


st.title('Walmart Unit Sales Forecasting')

@st.cache
def download_related_files():
    # "dataset" folder
    id = "1uGHaGby6g7PhxPGgMDzbts8AoYLPiv0M"
    gdown.download_folder(id=id, quiet=True, use_cookies=False)

    # "submission_csv" folder
    id = "1cdFdbFHWmGOGG8ssMsDsj2aFZMOhB0LC"
    gdown.download_folder(id=id, quiet=True, use_cookies=False)    

# Downloads the dataset files & prediction files
download_related_files()


dataset_path = './dataset/'
csv_path = './submission_csv/'
evaluation_df = pd.read_csv(dataset_path+'sales_train_evaluation.csv')

# s3.download_file('project-walmart-csv', 'submission_LightGBM.csv', './dataset/submission_LightGBM.csv')
# s3.download_file('project-walmart-csv', 'submission_LSTM.csv', './dataset/submission_LSTM.csv')
# s3.download_file('project-walmart-csv', 'submission_decisionTree.csv', './dataset/submission_decisionTree.csv')
# s3.download_file('project-walmart-csv', 'submission_MA.csv', './dataset/submission_MA.csv')
# s3.download_file('project-walmart-csv', 'submission_RandomForest.csv', './dataset/submission_RandomForest.csv')
# s3.download_file('project-walmart-csv', 'submission_SGD.csv', './dataset/submission_SGD.csv')
# s3.download_file('project-walmart-csv', 'submission_XGB.csv', './dataset/submission_XGB.csv')


# Item dropdown list
item_options = evaluation_df['id'].str.replace('_evaluation','').tolist()
# Dropdown Menu
selected_item = st.selectbox(label="Which Item you want to select?",\
             options = item_options,\
             label_visibility="visible")

# Model dropdown list
model_options = ['Decision Tree Model','LightGBM', 'Random Forest Model','XGBoost Regressor', 'Stochastic Gradient Descent Regressor', 'Moving Average', 'LSTM']
# Dropdown Menu
selected_model = st.selectbox(label="Which model you want check with?",\
             options = model_options,\
             label_visibility="visible")

if selected_model == 'Decision Tree Model':
    prediction_df = pd.read_csv(csv_path+'submission_decisionTree.csv')
    
if selected_model == 'LightGBM':
    prediction_df = pd.read_csv(csv_path+'submission_LightGBM.csv')
    
if selected_model == 'Random Forest Model':
    prediction_df = pd.read_csv(csv_path+'submission_RandomForest.csv')
    
if selected_model == 'XGBoost Regressor':
    prediction_df = pd.read_csv(csv_path+'submission_XGB.csv')
    
if selected_model == 'Stochastic Gradient Descent Regressor':
    prediction_df = pd.read_csv(csv_path+'submission_SGD.csv')
    
if selected_model == 'Moving Average':
    prediction_df = pd.read_csv(csv_path+'submission_MA.csv')
    
if selected_model == 'LSTM':
    prediction_df = pd.read_csv(csv_path+'submission_LSTM.csv')


def get_df_actual(evaluation_df,selected_item):
    # Getting Evaluation data and perticularly that Time-Series
    cols = [col for col in evaluation_df.columns if 'd_' in col] 
    given_series = evaluation_df[evaluation_df.id == selected_item+'_evaluation']
    given_series = given_series[cols]
    given_series = given_series.T
    given_series.columns = ['Actual']
    return given_series

def get_df_prediction(prediction_df,selected_item):
    future_series = prediction_df[prediction_df.id == selected_item+'_validation' ]
    future_series = future_series.set_index('id')
    future_series.columns = ['d_'+str(i) for i in range(1914,1942)]
    future_series = future_series.T
    future_series.columns = ['prediction']
    return future_series

# line plot for actual values
df = get_df_actual(evaluation_df,selected_item)
pred_df = get_df_prediction(prediction_df,selected_item)

# Merge both of them for shared X axis
df ['Prediction'] = pred_df['prediction']

df = df.reset_index()
# Melt it to conver it in tabular format
tabular_df = pd.melt(df, id_vars='index', value_vars=['Actual','Prediction'],var_name='type', value_name='unit_sales')

# Dropping Predition NaNs (From training day)
tabular_df.dropna(inplace=True)

# Actual units sold line
fig = px.line(tabular_df, x='index', y='unit_sales', color='type', markers=True, title="Time Series plot for "+selected_item, range_x=['d_1900','d_1941'])

st.plotly_chart(fig, use_container_width=True)
