import streamlit as st
import pandas as pd
import numpy as np
import gdown


st.title('Walmart Unit Sales Forecasting')

# "dataset" folder
id = "1uGHaGby6g7PhxPGgMDzbts8AoYLPiv0M"
gdown.download_folder(id=id, quiet=True, use_cookies=False)

# "submission_csv" folder
id = "1cdFdbFHWmGOGG8ssMsDsj2aFZMOhB0LC"
gdown.download_folder(id=id, quiet=True, use_cookies=False)


# data = "./data/police.csv"
# weather_data = "./weather.csv"
option = st.selectbox(
    'Select the item here',
    ('Email', 'Home phone', 'Mobile phone'))

with st.expander("See explanation"):
    st.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
    st.image("https://static.streamlit.io/examples/dice.jpg")
# @st.cache
# def load_data(path,nrows=10000):
#     data = pd.read_csv(path, nrows=nrows)
# #     lowercase = lambda x: str(x).lower()
# #     data.rename(lowercase, axis='columns', inplace=True)
# #     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data
  
