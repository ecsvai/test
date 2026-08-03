import pandas as pd
import streamlit as st


df = pd.read_csv('25-12kumamoto.csv',dtype=str)

df.dropna(how='all',inplace=True)

df['在留資格'] = df['在留資格'].str.split('：').str[1]

print(df['在留資格'].unique())

df.to_csv('25-12kumamoto.csv',index=False)









