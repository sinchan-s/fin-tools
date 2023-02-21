#! Important Libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np

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

tab1, tab2 = st.tabs(['SIP', 'HL'])

t1col1, t1col2 = tab1.columns(2)
sip_amt = t1col1.select_slider('Monthly Investment',[n for n in range(500,100000,500)])
interest_r = t1col1.select_slider('Expected Interest (%)',[round(i,1) for i in np.arange(0.5,30.1,0.1)])
time_period = t1col1.slider('Time Period',1,40)

returns_t = sip_amt*(((1 + interest_r/1200)**(time_period*12)-1)/(interest_r/1200))*(1+interest_r/1200)
invested = sip_amt*time_period*12
exp_return = round(returns_t-invested)
t1col2.metric('Total Invested', invested,)
t1col2.metric('Returns', exp_return,f'{round(exp_return*100/invested,2)}%')
t1col2.metric('Total Value', round(returns_t),f'{round(returns_t/invested,2)}x ')

pie_data = {'Exp. Returns': exp_return, 'Total Invested': invested}
fig2 = px.pie(values=pie_data.values(), names=pie_data.keys(), color=pie_data.keys(), hole=0.5)
t1col1.plotly_chart(fig2)