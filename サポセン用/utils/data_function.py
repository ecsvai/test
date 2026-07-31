import pandas as pd
import streamlit as st
import pathlib as pl

BASE_DIR = pl.Path(__file__).resolve().parent.parent
data_2512 = BASE_DIR / 'data'/'25-12kumamoto.csv'
data_2506 = BASE_DIR / 'data'/'25-06kumamoto.csv'
data_2412 = BASE_DIR / 'data'/'24-12kumamoto.csv'
data_2406 = BASE_DIR / 'data'/'24-06kumamoto.csv'
data_2312 = BASE_DIR / 'data'/'23-12kumamoto.csv'
data_2306 = BASE_DIR / 'data'/'23-06kumamoto.csv'
data_2212 = BASE_DIR / 'data'/'22-12kumamoto.csv'
data_2206 = BASE_DIR / 'data'/'22-06kumamoto.csv'
data_2112 = BASE_DIR / 'data'/'21-12kumamoto.csv'
data_2106 = BASE_DIR / 'data'/'21-06kumamoto.csv'


year_list = {
    '2025/12':data_2512,
    '2025/06':data_2506,
    '2024/12':data_2412,
    '2024/06':data_2406,
    '2023/12':data_2312,
    '2023/06':data_2306,
    '2022/12':data_2212,
    '2022/06':data_2206,
    '2021/12':data_2112,
    '2021/06':data_2106
}


@st.cache_data
def load_data():
    data = {}
    drop_cols = []
    for year in year_list:
        data[year] = pd.read_csv(year_list[year])
        data[year] = data[year].dropna(how='all')
        #drop_cols = data[year].columns.drop("在留外国人数",'')
        data[year] = data[year].ffill()
        if '市区町村コード' in data[year].columns:
            data[year] = data[year].drop(columns='市区町村コード')
    return data

def load_data_city_nat(year):
    data = {}
    data = pd.read_csv(BASE_DIR / 'data'/f'{year[:4]}-{year[5:7]}city_nat.csv', dtype=str)

    return data
