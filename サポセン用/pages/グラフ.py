import pandas as pd
import streamlit as st
import plotly.express as px


from utils.data_function import load_data
data = load_data()

def data_exact(year):
    return data[year]

type_select = st.selectbox('choose',['-','長期推移','特定の年'],key = 'type_select')

if type_select == '-':
    st.stop()


def reset():
    st.session_state['type_select'] = '-'

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
def bar_chart():
    fig_output = px.histogram(data_output, param_1, '在留外国人数', barmode='group', text_auto=True)
    fig_output.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig_output)

    fig_output = px.histogram(data_output2, param_1, '在留外国人数', color=param_2,
                              barmode='stack', text_auto=True)
    fig_output.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig_output)

type_chart = st.selectbox('チャート種類', ['-', '棒', '円'])



##Pie Chart#####################################
def pie_chart():
    if param_1 == '-' or param_2 == '-':
        st.stop()
    else:
        detailed_select = st.selectbox('Choose Pie Name',
                                       ['-']+list(data_output2[param_1].unique())
                                       , key = 'detailed_select')
        if detailed_select == "-":
            d_df = data_output2
        else:
            d_df = data_output2.loc[data_output2[param_1] == detailed_select]

        fig_output = px.pie(d_df, names=d_df[param_2], values='在留外国人数')
        st.dataframe(d_df)
        st.plotly_chart(fig_output)


if type_chart == '-':
    st.stop()
elif type_chart == '棒':
    bar_chart()
elif type_chart == '円':
    pie_chart()


##Chronological Order##########################