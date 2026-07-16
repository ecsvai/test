import pandas as pd
import streamlit as st
import pathlib as pl


st.caption('＊＊（注１）在留外国人数が5,000人未満の市町村に関しては、年齢及び性別に秘匿処理を行っています＊＊')
st.caption('＊＊（注２）総数10人以下の市町村については、人数以外の国籍・地域、在留資格、年齢及び性別については秘匿処理を行っています＊＊')
st.caption('＊＊（注３）2023年12月以前のデータは「市区町村」のクロスサーチができません。市区町村データはページの最下部にあります＊＊')

years = st.selectbox('年月を選択',
                     ['-','202512','202506','202412','202406','202312','202306',
                      '202212','202206','202112','202106'])

BASE_DIR = pl.Path(__file__).resolve().parent.parent

data_main = BASE_DIR / 'data'/f'{years[2:4]}-{years[4:6]}kumamoto.csv'
city_nat = BASE_DIR / 'data'/f'{years[:4]}-{years[4:6]}city_nat.csv'


@st.cache_data
def load_data(years):
    return pd.read_csv(data_main)




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
        ['全部', '熊本市全体']+list(full_table['市区町村'].unique()),
        key = 'city'
    )
    if city == '熊本市全体':
        result = result[result['市区町村'].isin([
            '熊本市中央区','熊本市東区','熊本市西区','熊本市南区','熊本市北区'])]
        result['市区町村'] = '熊本市全体'
    elif city != '全部':
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

if years <= '202306':
    with st.container(border = True):
        st.badge('市区町村x国籍・地域')
        st.dataframe((pd.read_csv(city_nat)))





