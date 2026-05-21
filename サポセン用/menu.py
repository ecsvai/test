import streamlit as st
import pathlib as pl

base_dir = pl.Path(__file__).resolve().parent

st.title('日本外国人統計データ')
st.write('総数＝中長期在留者及び特別永住者（短期滞在者が含まない）')
st.image(base_dir/'data'/'group_young_world.png')
st.balloons()


menu = st.sidebar
