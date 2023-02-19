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
    pass

def sip():
    pass

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Home Loan','SIP','NPS','Tab4','Dividends'])
tab1.button('Calculate Home Loan EMIs', on_click=hl_emi)

sip_amt = tab2.slider('Monthly Investment',500,100000)
interest_r = tab2.slider('Expected Return (p.a.)',0.1,30.0)
time_period = tab2.slider('Time Period',1,40)

returns_t = sip_amt*(((1 + interest_r/1200)**(time_period*12)-1)/(interest_r/1200))*(1+interest_r/1200)
tab2.metric('Invested',sip_amt*time_period*12)
tab2.metric('Returns',round(returns_t-sip_amt*time_period*12))
tab2.metric('Total Value',round(returns_t))

tab3.button('Calculate NPS returns', on_click=hl_emi)
tab4.button('Calculate  returns', on_click=sip)
tab5.button('Calculate dividends', on_click=hl_emi)