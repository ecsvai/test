import pandas as pd
import streamlit as st


df = pd.read_csv('2022-06city_nat.csv',dtype=str)

print(df.columns)
df = df.drop(columns=['Unnamed: 0'])
print(df.columns)

df.to_csv('2022-06city_nat.csv',index=False)

