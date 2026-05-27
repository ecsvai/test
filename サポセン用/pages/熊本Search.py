import pandas as pd
import streamlit as st
import pathlib as pl


BASE_DIR = pl.Path(__file__).resolve().parent.parent
data_2506 = BASE_DIR / 'data'/'25-06kumamoto.csv'
data_2406 = BASE_DIR / 'data'/'24-06kumamoto.csv'
data_2306_main = BASE_DIR / 'data'/'23-06kumamoto_main.csv'
data_2206_main = BASE_DIR / 'data'/'22-06kumamoto_main.csv'
data_2106_main = BASE_DIR / 'data'/'21-06kumamoto_main.csv'


st.caption('＊＊選択肢「-」＝「わからない」＊＊')
st.caption('2025のデータに熊本市以外の市町区村は「性別」・「年齢」の統計データがありません')
st.caption('2024以前のデータは「市町区村」のクロスサーチができません')

years = st.selectbox('Choose Year',
                     ['-','2025','2024','2023','2022','2021'])

year_list = {
    '2025':data_2506,
    '2024':data_2406,
    '2023':data_2306_main,
    '2022':data_2206_main,
    '2021':data_2106_main
}

@st.cache_data
def load_data(years):
    if years in year_list:
        return pd.read_csv(year_list[years])




if years == '-':
    full_table = None
    st.stop()

else:
    full_table = load_data(years)
    cols = full_table.columns.drop("在留外国人数")

full_table[cols] = full_table[cols].ffill()

if "市区町村コード" in full_table.columns:
    full_table = full_table.drop(columns = '市区町村コード')


keys = ['city','qual','sex','age5sai','pref','nat']
def reset():
    for key in keys:
        st.session_state[key] = '全部'
st.button('reset',on_click=reset)

result = full_table

filter_text = ''

if '市区町村' in result.columns:
    city = st.selectbox(
        '市区町村',
        ['全部']+list(full_table['市区町村'].unique()),
        key = 'city'
    )
    if city != '全部':
        result = result[result['市区町村'] == city]
        filter_text = '\n市区町村=' + city

if '年齢（５歳階級）' in result.columns:
    age5sai = st.selectbox(
        '年齢（５歳階級）',
        ['全部']+list(full_table['年齢（５歳階級）'].unique()),
        key = 'age5sai'
    )
    if age5sai != '全部':
        result = result[result['年齢（５歳階級）']==age5sai]
        filter_text += '\n年齢（５歳階級）=' + age5sai

if '性別' in result.columns:
    sex = st.selectbox(
        '性別',
        ['全部']+list(full_table['性別'].unique()),
        key = 'sex'
    )
    if sex != '全部':
        result = result[result['性別']==sex]
        filter_text += '\n性別=' + sex

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




if nat != '全部':
    result = result[result['国籍・地域'] == nat]
    filter_text += '\n国籍・地域=' + nat

if qual != '全部':
    result = result[result['在留資格'] == qual]
    filter_text += '\n在留資格=' + qual


result['在留外国人数'] = pd.to_numeric(
    result['在留外国人数'].astype(str).str.replace(',', ''),
    errors='coerce'
)


st.divider()
st.header('総数＝'+str(result['在留外国人数'].sum()))
st.divider()
st.code('filter:' + filter_text)

for x in result.columns.drop(['在留外国人数','都道府県']):
    st.badge('順位表（'+x+'）')
    st.dataframe(result.groupby(x).sum()['在留外国人数'].sort_values(ascending=False))



