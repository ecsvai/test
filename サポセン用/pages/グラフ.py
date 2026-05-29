import pandas as pd
import streamlit as st
import plotly.express as px


from utils.data_function import load_data
data = load_data()

def data_exact(year):
    return data[year]

type_select = st.selectbox('choose',['-','長期推移','特定の年'],key = 'type_select')
type_chart = st.selectbox('チャート種類', ['-', '棒', '円','折れ線'], key='type_chart')

if type_select == '-':
    st.stop()


def reset():
    st.session_state['type_select','type_chart'] = '-'

st.button('reset',on_click=reset)


## Selected Year########################3
if type_select == '特定の年':
    year_exact = st.selectbox('Choose Year',['-','2025','2024','2023','2022','2021'], key = 'year_exact')
    if year_exact == '-':
        st.stop()
    else:
        data_current = data_exact(year_exact)

    param_1 = st.selectbox('Select Parameter 1',
                           ['-']+
                           list(data_current.columns.drop('在留外国人数')),key = 'param_1')
    check_top10 = st.checkbox('Show Top 10', key='param_1_checkbox')

    param_2 = st.selectbox('Select Parameter 2',
                           ['-']
                           +list(data_current.columns.drop('在留外国人数')), key = 'param_2')
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
            data_output = data_top10.copy()



    if param_2 != '-':

        data_temp_2 = ((data_current[[param_1, param_2, '在留外国人数']]
                      .copy()
                      .groupby([param_1,param_2], as_index=False)
                        ['在留外国人数'].sum()
                      .sort_values([param_1,'在留外国人数'], ascending=False))
                     )


        city_total = data_temp.rename(columns = {'在留外国人数': 'total'})
        data_temp_2 = data_temp_2.merge(city_total, on = param_1)
        data_temp_2 = data_temp_2.sort_values(['total',param_1,'在留外国人数'],ascending=False).drop(columns = 'total')
        data_output2 = data_temp_2.copy()

        if check_top10_2:
            top10_2 = data_temp_2[param_1].unique()[:10]
            data_top10_2 = data_temp_2.loc[data_temp_2[param_1].isin(top10_2)]
            top10_2_2 = pd.DataFrame()
            for x in top10_2:
                top10_2_2 = pd.concat(
                    [top10_2_2,data_top10_2.loc[data_top10_2[param_1]==x][:10]],ignore_index=True)

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
        else:
            detailed_select = st.selectbox('Choose Pie Name',
                                           ['-']+list(data_output2[param_2].unique())
                                           , key = 'detailed_select')
            if detailed_select == "-":
                d_df = data_output2
            else:
                d_df = data_output2.loc[data_output2[param_2] == detailed_select]

        fig_output = px.pie(d_df, names=d_df[param_1], values='在留外国人数')
        st.plotly_chart(fig_output)
#####################################################

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
    for year in ['2025','2024','2023','2022','2021']:
        df_total = data_exact(year).copy()
        df_total['year'] = year
        df_final = pd.concat([df_final,df_total])

    param_1 = st.selectbox('Select Parameter 1',
                           ['-'] +
                           list(df_final.columns.drop(['在留外国人数','year'])), key='param_1')

    df_change = df_final.groupby([param_1, 'year'], as_index= False)['在留外国人数'].sum()

    df_temp = pd.DataFrame()
    df_temp['year'] = df_final['year'].unique().astype(int)
    total_list = []
    for x in df_final['year'].unique():
        total_list.append(df_final.loc[df_final['year'] == x]['在留外国人数'].sum())
    df_temp['total'] = total_list

    fig_output = px.line(df_temp,x = 'year', y = 'total', markers = True)
    fig_output.update_xaxes(tickformat = 'd', type = 'category', categoryorder = 'total ascending')
    st.plotly_chart(fig_output)

    if param_1 == '-':
       st.stop()
    elif param_2 == '-':
        pass
    else:
        param_2 = st.selectbox('Select Parameter 2', ['-'] + df_change[param_1].unique())






    st.dataframe(df_change)