
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

#! Tabs declaration
tab1, tab2 = st.tabs(['SIP Returns', 'Loan Calculator'])

#! Tab1 contents:
#?Tab1 slider controls
t1col1, t1col2 = tab1.columns(2)
sip_amt = t1col1.select_slider('Monthly Investment',[n for n in range(500, 100500, 500)])
interest_r = t1col1.select_slider('Expected Interest (%)',[round(i,1) for i in np.arange(0.5, 30.1, 0.1)])
time_period = t1col1.slider('Time Period', 1, 40)
#?Tab1 calculations & metric display
returns_t = sip_amt*(((1 + interest_r/1200)**(time_period*12)-1)/(interest_r/1200))*(1+interest_r/1200)
invested = sip_amt*time_period*12
exp_return = round(returns_t-invested)
t1col2.metric('Total Invested', invested,)
t1col2.metric('Returns', exp_return,f'{round(exp_return*100/invested,2)}%')
t1col2.metric('Total Value', round(returns_t),f'{round(returns_t/invested,2)}x ')
#?Tab1 pie chart
pie_data = {'Expected Returns': exp_return, 'Total Invested': invested}
fig1 = px.pie(values=pie_data.values(), names=pie_data.keys(), color=pie_data.keys(), labels=pie_data.keys(), title='Invested vs Returns', hole=0.4, color_discrete_sequence=px.colors.sequential.Bluered)
t1col1.plotly_chart(fig1)

#! Tab2 contents:
#?Tab2 slider controls
t2col1, t2col2 = tab2.columns(2)
loan_amt = t2col1.select_slider('Monthly Investment',[n for n in range(100000, 10000000, 50000)])
interest_l = t2col1.select_slider('Loan Interest (%)',[round(i,1) for i in np.arange(1.0, 30.1, 0.1)])
tenure = t2col1.slider('Time Period', 1, 30)
#?Tab2 calculations & metric display
emi_amt = loan_amt*(interest_l/1200)*(1+interest_l/1200)**(tenure*12)/((1+interest_l/1200)**(tenure*12)-1)
loan_plus_int = emi_amt*tenure*12
interest_amt = round(loan_plus_int-loan_amt)
int_per_loan = round(interest_amt/loan_amt,2)
t2col2.metric('Monthly EMI', round(emi_amt),)
t2col2.metric('Principal Amount', loan_amt,)
t2col2.metric('Total Interest', round(interest_amt),f'{int_per_loan*100}%')
t2col2.metric('Total Value', round(loan_plus_int),f'{int_per_loan}x')
#?Tab2 pie chart
pie_data = {'Interest Amount': interest_amt, 'Principal Amount': loan_amt}
fig2 = px.pie(values=pie_data.values(), names=pie_data.keys(), color=pie_data.keys(), labels=pie_data.keys(), title='Principal vs Loan Interest', hole=0.6, color_discrete_sequence=px.colors.diverging.Portland)
t2col1.plotly_chart(fig2)
