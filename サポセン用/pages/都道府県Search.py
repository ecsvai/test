import pandas as pd
import streamlit as st
import pathlib as pl

base_dir = pl.Path(__file__).resolve().parent.parent
file_path = base_dir / 'data'/'25-06full table source.csv'

@st.cache_data
def load_data():
    return pd.read_csv(file_path, header=0)

full_table = load_data()

st.title('都道府県別で探す！')

keys = ['nat','qual','sex','age5sai','pref']
def reset():
    for key in keys:
        st.session_state[key] = '全部'
st.button('reset',on_click=reset)

result = full_table

nat = st.selectbox(
    "国籍・地域",
    ['全部']+list(full_table['国籍/地域'].sort_values().unique()),
    key = 'nat'
)

qual = st.selectbox(
    "在留資格",
    ['全部']+list(full_table['在留資格'].sort_values().unique()),
    key = 'qual'
)

sex = st.selectbox(
    "性別",
    ['全部']+list(full_table['性別'].sort_values().unique()),
    key = 'sex'
)

age5sai = st.selectbox(
    "年齢（５歳階級）",
    ['全部']+list(full_table['年齢（５歳階級）'].sort_values().unique()),
    key = 'age5sai'
)

pref = st.selectbox(
    "都道府県",
    ['全部']+list(full_table['都道府県'].sort_values().unique()),
    key = 'pref'
)

if nat != '全部':
    result = result[result['国籍/地域'] == nat]

if qual != '全部':
    result = result[result['在留資格'] == qual]

if sex != '全部':
    result = result[result['性別'] == sex]

if age5sai != '全部':
    result = result[result['年齢（５歳階級）'] == age5sai]

if pref != '全部':
    result = result[result['都道府県'] == pref]

st.divider()
st.header('総数 = '+ str(result['在留外国人数'].sum()))



