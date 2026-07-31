import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import pathlib as pl

base_dir = pl.Path(__file__).resolve().parent.parent

from utils.data_function import load_data
from utils.data_function import load_data_city_nat
data = load_data()

def data_exact(year):
    return data[year]

st.header('メンテナンス中！')
st.image(base_dir/'data'/'ojigi.png')
st.error('メンテナンス中！')
st.divider()

#st.caption('性別・年齢のデータが不十分のため使わないでください')
#st.caption('市区町村のデータは2024/2025年のみ')



type_select = st.selectbox('データを選択',['-','長期推移','特定の年'],key = 'type_select')


if type_select == '-':
    st.stop()


def reset():
    st.session_state['type_select'] = '-'

st.button('reset',on_click=reset)


## Selected Year########################3
if type_select == '特定の年':
    year_exact = st.selectbox('年月',['-','2025/12','2025/06','2024/12','2024/06','2023/12',
                                      '2023/06','2022/12','2022/06','2021/12','2021/06'], key = 'year_exact')
    type_chart = st.selectbox('グラフの種類', ['-', '棒', '円'], key='type_chart')
    if year_exact == '-':
        st.stop()
    else:
        data_current = data_exact(year_exact)

    param_1 = st.selectbox('フィルター１を選択',
                           ['-']+
                           list(data_current.columns.drop(['在留外国人数','都道府県'])),key = 'param_1')
    check_top10 = st.checkbox('Show Top 10', key='param_1_checkbox')

    param_2 = st.selectbox('フィルター２を選択',
                           ['-']
                           +list(data_current.columns.drop(['在留外国人数','都道府県'])), key = 'param_2')
    check_top10_2 = st.checkbox('Show Top 10', key='param_2_checkbox')

    if param_1 == '-':
        st.stop()
    elif param_1 == param_2:
        st.stop()
    elif param_1 != '-':

        data_temp = ((data_current[[param_1,'在留外国人数']]
                     .copy()
                     .groupby(param_1,as_index = False)['在留外国人数'].sum()
                     .sort_values('在留外国人数',ascending=False))
                     )
        data_output = data_temp.copy()

        if check_top10:
            top10 = data_temp[param_1].head(10).unique()
            data_top10 = data_temp.loc[data_temp[param_1].isin(top10)]
            other = data_temp.loc[~data_temp[param_1].isin(top10)].sum(numeric_only=True)
            other[param_1] = 'その他'

            data_output = data_top10.copy()
            data_output.loc[len(data_output)] = other





    if param_2 != '-':

        data_temp_2 = ((data_current[[param_1, param_2, '在留外国人数']]
                      .copy()
                      .groupby([param_1,param_2], as_index=False)
                        ['在留外国人数'].sum()
                      .sort_values([param_1,'在留外国人数'], ascending=False))
                     )


        city_total = data_temp.rename(columns = {'在留外国人数': 'total'})
        data_temp_2 = data_temp_2.merge(city_total, on = param_1)
        data_temp_2 = (data_temp_2.sort_values(['total',param_1,'在留外国人数'],ascending=False)
                       .drop(columns = 'total'))
        data_output2 = data_temp_2.copy()


        if check_top10_2:
            top10_2 = data_temp_2[param_1].unique()[:10]
            data_top10_2 = data_temp_2.loc[data_temp_2[param_1].isin(top10_2)]
            top10_2_2 = pd.DataFrame()
            for x in top10_2:
                top10_2_2 = pd.concat(
                    [top10_2_2,
                     data_top10_2.loc[data_top10_2[param_1]==x][:10]],ignore_index=True)





            data_output2 = top10_2_2.copy()





    ##Bar chart####################################
    def bar_chart_specific_year():
        fig_output = px.histogram(data_output, param_1, '在留外国人数', barmode='group', text_auto=True)
        fig_output.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_output)
        if param_2 != '-':
            fig_output = px.histogram(data_output2, param_1, '在留外国人数', color=param_2,
                                      barmode='stack', text_auto=True)
            fig_output.update_layout(xaxis={'categoryorder': 'total descending'})
            st.plotly_chart(fig_output)





    ##Pie Chart#####################################
    def pie_chart_specific_year():

        if param_1 == '-':
            st.stop()
        elif param_2 == '-':
            d_df = data_output
            fig_output = px.pie(d_df, names=d_df[param_1], values='在留外国人数')
            st.plotly_chart(fig_output)
        else:
            detailed_select = st.selectbox('Select Value for Parameter 2',
                                           ['-']+list(data_temp_2[param_2].unique())
                                           , key = 'detailed_select')
            if detailed_select == "-":
                d_df = data_output
            elif detailed_select != '-' and check_top10_2 == False:
                d_df = data_temp_2.loc[data_temp_2[param_2] == detailed_select]
            elif detailed_select != '-' and check_top10_2 == True:
                d_df = data_temp_2.loc[data_temp_2[param_2] == detailed_select]
                top_d_df = d_df[param_1].unique()[:10]
                d_df = d_df[d_df[param_1].isin(top_d_df)]



            fig_output = px.pie(d_df, names=d_df[param_1], values='在留外国人数')
            st.plotly_chart(fig_output)
#####################################################

    st.divider()

    if type_chart == '棒':
        bar_chart_specific_year()
    elif type_chart == '円':
        pie_chart_specific_year()
    else:
        pass




##Chronological Order##########################

if type_select == '長期推移':
    df_total = pd.DataFrame()
    df_final = pd.DataFrame()
    for year in ['2025/12','2025/06','2024/12','2024/06','2023/12',
                 '2023/06','2022/12','2022/06','2021/12','2021/06']:
        df_total = data_exact(year).copy()
        df_total['year'] = year
        df_final = pd.concat([df_final,df_total])



    df_temp = pd.DataFrame()
    df_temp['year'] = df_final['year'].unique()
    total_list = []
    for x in df_final['year'].unique():
        total_list.append(df_final.loc[df_final['year'] == x]['在留外国人数'].sum())
    df_temp['total'] = total_list

    st.subheader('熊本県在留外国人総数推移')
    fig_output = px.line(df_temp,x = 'year', y = 'total', markers = True)
    fig_output.update_xaxes(tickformat = 'd', type = 'category',
                            categoryorder = 'category ascending')
    fig_output.update_yaxes(rangemode = 'tozero')
    st.plotly_chart(fig_output)

    st.divider()
    st.subheader('カテゴリーから探す')


    param_1 = st.selectbox('フィルター１を選択',
                           ['-'] +
                           list(df_final.columns.drop(['在留外国人数', 'year'])), key='param_1')


    if param_1 == '-':
       st.stop()
    else:
        df_change = df_final.groupby([param_1, 'year'], as_index=False)['在留外国人数'].sum()
        for y in ['2023/06','2022/12','2022/06', '2021/12','2021/06']:
            df_temp2 = load_data_city_nat(y)
            for x in df_change[param_1].unique():
                city_nat = df_temp2[df_temp2[param_1] == x]['総数'].iloc[0]

                df_change.loc[len(df_change)] = [x, y, city_nat]

        param_2 = st.multiselect('フィルター２を選択', df_change[param_1].unique())
        df_plot = df_change[df_change[param_1].isin(param_2)].sort_values('year', ascending=[False])




    fig_output2 = px.line(df_plot, x = 'year', y = '在留外国人数', color = param_1, markers = True)
    fig_output2.update_xaxes(categoryorder = 'category ascending')
    fig_output2.update_yaxes(rangemode = 'tozero')
    st.plotly_chart(fig_output2)




    #st.dataframe(df_final)
    #st.dataframe(df_change)