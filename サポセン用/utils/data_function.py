import pandas as pd
import streamlit as st
import pathlib as pl

year_vari = None

BASE_DIR = pl.Path(__file__).resolve().parent.parent
data_2506 = BASE_DIR / 'data'/'25-06kumamoto.csv'
data_2406 = BASE_DIR / 'data'/'24-06kumamoto.csv'
data_2306_main = BASE_DIR / 'data'/'23-06kumamoto_main.csv'
data_2206_main = BASE_DIR / 'data'/'22-06kumamoto_main.csv'
data_2106_main = BASE_DIR / 'data'/'21-06kumamoto_main.csv'

data_city_nat = BASE_DIR / 'data'/f'{year_vari}-06city_nat.csv'

year_list = {
    '2025':data_2506,
    '2024':data_2406,
    '2023':data_2306_main,
    '2022':data_2206_main,
    '2021':data_2106_main
}



@st.cache_data
def load_data():
    data = {}
    drop_cols = []
    for year in year_list:
        data[year] = pd.read_csv(year_list[year])
        drop_cols = data[year].columns.drop("在留外国人数",'')
        data[year] = data[year].ffill()
        if '市区町村コード' in data[year].columns:
            data[year] = data[year].drop(columns='市区町村コード')
    return data

#def load_data_city_nat():
    data = {}
    data_temp = {}
    for year in ['2023','2022','2021']:
        year_vari = year
        data = pd.read_csv(data_city_nat)
        data = data[year].groupby('市区町村')['総数'].sum().copy()

    return data
