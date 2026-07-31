import pandas as pd
import streamlit as st


df = pd.read_csv('2023-06city_nat.csv',dtype=str)

df.dropna(how='all',inplace=True)

df = df.rename(columns={'都道府県市区町村':'市区町村'})

print(df.columns)

df.to_csv('2023-06city_nat.csv',index=False)








