import pandas as pd
import streamlit as st


df = pd.read_csv('25-12kumamoto.csv',dtype=str)


df.dropna(how='all',axis=1,inplace=True)

df.to_csv('25-12kumamoto.csv',index=False)


