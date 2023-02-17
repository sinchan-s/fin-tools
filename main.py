#! Important Libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

#! Basic configurations
st.set_page_config(
    page_title="Fin-Tools",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed")

#! App header
st.header("Welcome to the solutions everything related to money")

def hl_emi():
    st.balloons()

def sip():
    st.snow()

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Home Loan','SIP','NPS','Tab4','Dividends'])
tab1.button('Calculate Home Loan EMIs', on_click=hl_emi)
tab2.button('Calculate SIP returns', on_click=sip)
tab3.button('Calculate NPS returns', on_click=hl_emi)
tab4.button('Calculate  returns', on_click=sip)
tab5.button('Calculate dividends', on_click=hl_emi)