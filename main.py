
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

#! Clean Footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#! App header
st.title("Welcome to the solutions everything related to money")

#! tax calculator class
class calc_tax:
    def __init__(self,net_sal, slab, slab_int, slab2, tax_rate, *args):
        self.net_sal = net_sal
        self.slab = slab
        self.slab_int = slab_int
        self.slab2 = slab2
        self.tax_rate = tax_rate
        self.tax_list = args
    def tax_slab1(self):
        tax1 = round(0 if self.net_sal<self.slab*tenK else (self.net_sal-self.slab*tenK)*self.slab_int if self.net_sal>self.slab*tenK and self.net_sal<self.slab2*tenK else self.tax_rate*tenK)
        return tax1
    def tax_slab2(self):
        tax2 = round(0 if self.net_sal<self.slab*tenK else (self.net_sal-self.slab*tenK)*self.slab_int)
        return tax2
    def cess4(self):
        cess = round(0 if net_sal<self.slab2*tenK else sum(self.tax_list)*0.04)
        return cess

#! Tabs declaration
tab1, tab2, tab3 = st.tabs(['SIP Returns', 'Loan EMI', 'Know Your Tax'])

#! Tab1 contents:
#?Tab1 slider controls
t1col1, t1col2 = tab1.columns(2)
sip_amt = t1col1.select_slider('Monthly Investment',[n for n in np.arange(100, 100500, 100)])
interest_r = t1col1.select_slider('Expected Interest (%)',[round(i,1) for i in np.arange(0.5, 30.1, 0.1)])
time_period = t1col1.slider('Time Period', 1, 40)
#?Tab1 calculations & metric display
returns_t = sip_amt*(((1 + interest_r/1200)**(time_period*12)-1)/(interest_r/1200))*(1+interest_r/1200)
invested = sip_amt*time_period*12
exp_return = round(returns_t-invested)
t1col2.metric('Total Invested', f'₹ {invested:,}',)
t1col2.metric('Returns', f'₹ {exp_return:,}',f'{round(exp_return*100/invested,2)}%')
t1col2.metric('Total Value', f'₹ {round(returns_t):,}',f'{round(returns_t/invested,2)}x ')
#?Tab1 pie chart
colors = ['darkorange', 'lightgreen']
pie_data = {'Expected Returns': exp_return, 'Total Invested': invested}
fig1 = px.pie(values=pie_data.values(), names=pie_data.keys(), labels=pie_data.keys(), title='Invested vs Returns', hole=0.6, width=500, height=500)
fig1.update_traces(textposition='outside', textinfo='percent', marker=dict(colors=colors, line=dict(color='#000000', width=2)))
t1col1.plotly_chart(fig1)

#! Tab2 contents:
#?Tab2 slider controls
t2col1, t2col2 = tab2.columns(2)
loan_amt = t2col1.select_slider('Principal Amount',[n for n in range(50000, 10050000, 50000)])
interest_l = t2col1.select_slider('Loan Interest (%)',[round(i,1) for i in np.arange(1.0, 30.1, 0.1)])
tenure = t2col1.slider('Tenure', 1, 30)
#?Tab2 calculations & metric display
emi_amt = loan_amt*(interest_l/1200)*(1+interest_l/1200)**(tenure*12)/((1+interest_l/1200)**(tenure*12)-1)
loan_plus_int = round(emi_amt*tenure*12)
interest_amt = loan_plus_int-loan_amt
int_per_loan = round(interest_amt/loan_amt,2)
t2col2.metric('Monthly EMI', f'₹ {round(emi_amt):,}',)
t2col2.metric('Total Interest', f'₹ {interest_amt:,}',f'{round(int_per_loan*100,2)}%')
t2col2.metric('Total Value', f'₹ {loan_plus_int:,}',f'{int_per_loan}x')
#?Tab2 pie chart
colors = ['gold', 'mediumturquoise']
pie_data = {'Interest Amount': interest_amt, 'Principal Amount': loan_amt}
fig2 = px.pie(values=pie_data.values(), names=pie_data.keys(), labels=pie_data.keys(), title='Principal vs Loan Interest', hole=0.6, width=500, height=500)
fig2.update_traces(textposition='outside', textinfo='percent', marker=dict(colors=colors, line=dict(color='#000000', width=2)))
t2col1.plotly_chart(fig2)

#! Tab3 contents:
#?Tab3 variables
tenK = 10000

#?Tab3 tax regime selection
t3col1, t3col2 = tab3.columns(2)
sal = t3col1.number_input("Salary Received",10*tenK,1000*tenK)
tax_regime = t3col2.radio('Choose your Tax regime:',["Old Tax Regime","New Tax Regime"])

#?Tab3 exemptions & deductions
t3col1.subheader("Exemptions")
hra = t3col1.number_input("HRA",0,100*tenK)
pt = t3col1.number_input("Professional Tax",0,tenK)
hl = t3col1.number_input("Housing Loan Interest",0,tenK)
std_dedct = 5*tenK
gross_sal = round(sal-hra-pt-hl-std_dedct)
gross_sal_display = t3col1.metric("Gross Total Income (with ₹ 50000 standard deduction)",f'₹ {gross_sal:,}')
t3col2.subheader("Deductions")
c80 = t3col2.number_input("Section 80C (LIC, ELSS, PPF etc.)",0,100*tenK)
ccd80 = t3col2.number_input("Section 80CCD (NPS Employee Contribution only)",0,100*tenK)
d80 = t3col2.number_input("Section 80D (Medical Insurance Premium of Self & Parents)",0,100*tenK)
net_sal = round(gross_sal-(c80 if c80<15*tenK else 15*tenK)-(ccd80 if ccd80<5*tenK else 5*tenK)-(d80 if ccd80<10*tenK else 10*tenK))
t3col2.metric("Net Taxable Income",f'₹ {net_sal:,}')

#?Tab3 tax calculation on regime basis
if tax_regime == "Old Tax Regime":
    t5 = calc_tax(net_sal, 25, 0.05, 50, 1.25)
    tax5 = t5.tax_slab1()
    t20 = calc_tax(net_sal, 50, 0.2, 100, 10)
    tax20 = t20.tax_slab1()
    t30 = calc_tax(net_sal, 100, 0.3, 0, 0)
    tax30 = t30.tax_slab2()
    c4 = calc_tax(net_sal, 0, 0, 50, 0, tax5, tax20, tax30)
    cess = c4.cess4()
    rebate = round(0 if net_sal>50*tenK else tax5)
    t3col1.subheader(f"Up to ₹ 2.5 lakh @ 0% = ₹ 0")
    t3col2.subheader(f"₹ 2,50,001 to ₹ 5 lakh @ 5% = ₹ {tax5:,}")
    t3col1.subheader(f"₹ 5,00,001 to ₹ 10 lakh @ 20% = ₹ {tax20:,}")
    t3col2.subheader(f"Over ₹ 10 lakh @ 30% = ₹ {tax30:,}")
    t3col1.subheader(f"Cess @ 4% = ₹ {cess:,}")
    t3col2.subheader(f"Tax Rebate = ₹ {rebate:,}")
    t3col1.metric("Your Tax",f'₹ {round(tax5+tax20+tax30+cess-rebate):,}')
else:
    t5 = calc_tax(net_sal, 30, 0.05, 60, 1.5)
    tax5 = t5.tax_slab1()
    t10 = calc_tax(net_sal, 60, 0.1, 90, 3)
    tax10 = t10.tax_slab1()
    t15 = calc_tax(net_sal, 90, 0.15, 120, 4.5)
    tax15 = t15.tax_slab1()
    t20 = calc_tax(net_sal, 120, 0.2, 150, 6)
    tax20 = t20.tax_slab1()
    t30 = calc_tax(net_sal, 150, 0.3, 0, 0)
    tax30 = t30.tax_slab2()
    c4 = calc_tax(net_sal, 0, 0, 50, 0, tax5, tax10, tax15, tax20, tax30)
    cess = c4.cess4()
    rebate = round(0 if net_sal>70*tenK else tax5+tax10)
    t3col1.subheader(f"Up to ₹ 3 lakh @ 0% = ₹ 0")
    t3col2.subheader(f"₹ 3,00,001 to ₹ 6 lakh @ 5% = ₹ {tax5:,}")
    t3col1.subheader(f"₹ 6,00,001 to ₹ 9 lakh @ 10% = ₹ {tax10:,}")
    t3col2.subheader(f"₹ 9,00,001 to ₹ 12 lakh @ 15% = ₹ {tax15:,}")
    t3col1.subheader(f"₹ 12,00,001 to ₹ 15 lakh @ 20% = ₹ {tax20:,}")
    t3col2.subheader(f"Over ₹ 15 lakh @ 30% = ₹ {tax30:,}")
    t3col1.subheader(f"Cess @ 4% = ₹ {cess:,}")
    t3col2.subheader(f"Tax Rebate = ₹ {rebate:,}")
    t3col1.metric("Your Tax",f'₹ {round(tax5+tax10+tax15+tax20+tax30+cess-rebate):,}')