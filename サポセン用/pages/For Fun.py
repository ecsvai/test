import streamlit as st

def balloons():
    st.balloons()

def snow():
    st.snow()
st.button('Balloon',on_click=balloons)
st.button('Snow',on_click=snow)