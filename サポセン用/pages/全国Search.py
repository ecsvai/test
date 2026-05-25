import pandas as pd
import streamlit as st
import pathlib as pl

base_dir = pl.Path(__file__).resolve().parent.parent
data_path = base_dir / 'data'/'25-06年齢・性別別.xlsx'
data_path2 = base_dir / 'data'/'25-06国籍・地域・資格別.xlsx'

agesex = pd.read_excel(data_path, header=3)
natqual = pd.read_excel(data_path2, header=3)



maintable = {
    '年齢・性別別': agesex,
    '国籍・地域・在留資格別': natqual,
}

select_form = st.selectbox('choose criteria', maintable.keys())
result = maintable[select_form]

if  select_form == '国籍・地域・在留資格別':
    continent = st.selectbox(
        '州',
        natqual['州'].unique()
    )
    result = result[result['州'] == continent]

    if continent != '総数':
        natreg = st.selectbox(
            '国籍・地域',
            result['国籍・地域'].unique()
        )
        result = result[result['国籍・地域'] == natreg]
    else:
        natreg = st.selectbox(
            '国籍・地域',
            natqual['国籍・地域'].unique()
        )

        result = natqual[natqual['国籍・地域'] == natreg]

    qual = st.selectbox(
       '在留資格',
        natqual['在留資格'].unique()
    )
    result = result[result['在留資格'] == qual]
    st.write(result)



if  select_form == '年齢・性別別':
    continent = st.selectbox(
        '州',
        agesex['州'].unique()
    )
    result = result[result['州'] == continent]

    if continent != '総数':
        natreg = st.selectbox(
            '国籍・地域',
            result['国籍・地域'].unique()
        )
        result = result[result['国籍・地域'] == natreg]
    else:
        natreg = st.selectbox(
            '国籍・地域',
            natqual['国籍・地域'].unique()
        )
    age = st.selectbox(
        '年齢',
        agesex['年齢'].unique()
    )
    result = result[result['年齢'] == age]
    sex = st.selectbox(
        '性別',
        agesex['性別'].unique()
    )
    result = result[result['性別'] == sex]

    st.divider()
    st.write(result)