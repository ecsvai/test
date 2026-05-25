import pandas as pd
import streamlit as st
import pathlib as pl

BASE_DIR = pl.Path(__file__).resolve().parent.parent
data_path = BASE_DIR / 'data'/'25-06kumamoto.csv'

st.write('＊＊選択肢「-」＝「わからない」＊＊')
st.write('熊本市以外の市町村は「性別」・「年齢」の統計データがありません')

@st.cache_data
def load_data():
    return pd.read_csv(data_path, header=0)

full_table = load_data()

keys = ['city','qual','sex','age5sai','pref','nat']
def reset():
    for key in keys:
        st.session_state[key] = '全部'
st.button('reset',on_click=reset)

full_table[[
    '都道府県','市区町村','年齢（５歳階級）','性別','国籍・地域']] = (
    full_table[[
    '都道府県','市区町村','年齢（５歳階級）','性別','国籍・地域']].ffill())

result = full_table

filter_text = ''



city = st.selectbox(
    '市区町村',
    ['全部']+list(full_table['市区町村'].unique()),
    key = 'city'
)

age5sai = st.selectbox(
    '年齢（５歳階級）',
    ['全部']+list(full_table['年齢（５歳階級）'].unique()),
    key = 'age5sai'
)

sex = st.selectbox(
    '性別',
    ['全部']+list(full_table['性別'].unique()),
    key = 'sex'
)

nat = st.selectbox(
    "国籍・地域",
    ['全部']+list(full_table['国籍・地域'].sort_values().unique()),
    key = 'nat'
)

qual = st.selectbox(
    "在留資格",
    ['全部']+list(full_table['在留資格'].sort_values().unique()),
    key = 'qual'
)

if city != '全部':
    result = result[result['市区町村']==city]
    filter_text = '\n市区町村=' + city

if age5sai != '全部':
    result = result[result['年齢（５歳階級）']==age5sai]
    filter_text += '\n年齢（５歳階級）=' + age5sai

if sex != '全部':
    result = result[result['性別']==sex]
    filter_text += '\n性別=' + sex

if nat != '全部':
    result = result[result['国籍・地域'] == nat]
    filter_text += '\n国籍・地域=' + nat

if qual != '全部':
    result = result[result['在留資格'] == qual]
    filter_text += '\n在留資格=' + qual


result['合計 / 在留外国人数'] = pd.to_numeric(
    result['合計 / 在留外国人数'].astype(str).str.replace(',', ''),
    errors='coerce'
)


st.divider()
st.header('総数＝'+str(result['合計 / 在留外国人数'].sum()))
st.divider()
st.code('filter:' + filter_text)


st.dataframe(result.groupby('在留資格').sum()['合計 / 在留外国人数'].sort_values(ascending=False))


st.dataframe(result.groupby('市区町村').sum()['合計 / 在留外国人数'].sort_values(ascending=False))

