
#! Important Libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np
import numpy_financial as npf

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

#! Tax calculator class
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

#! Loan amortization schedule function
def amort(loan_amt, interest_l, loan_tenure, emi_amt):
    months = []
    principle_2_loan = []
    interest_2_loan = []
    loan_emi = []
    loan_balance = []
    bal_amt = loan_amt
    for i in range(loan_tenure):
        month = i + 1
        pcpl_amt = npf.ppmt(interest_l/1200, month, loan_tenure, -loan_amt)
        int_amt = emi_amt - pcpl_amt
        bal_amt -= pcpl_amt
        principle_2_loan.append(round(pcpl_amt))
        interest_2_loan.append(round(int_amt))
        loan_emi.append(round(emi_amt))
        loan_balance.append(round(bal_amt))
        months.append(month)
    return months, principle_2_loan, interest_2_loan, loan_emi, loan_balance

#! Tabs declaration
tab1, tab2, tab3, tab4 = st.tabs(['SIP Returns', 'Any Loan EMI', 'Know Your Tax', 'PPF Calculator'])

#! Tab1 contents:
#?Tab1 columns defined
with tab1:
    col1, col2 = st.columns(2)
    
    #?Tab1 slider controls
    with col1:
        sip_amt = st.select_slider('Monthly Investment',[n for n in np.arange(100, 100100, 100)])
        interest_r = st.select_slider('Expected Interest (%)',[round(i,1) for i in np.arange(0.5, 30.1, 0.1)])
        time_period = st.slider('Time Period', 1, 40)

    #?Tab1 calculations & metric display
    returns_t = sip_amt*(((1 + interest_r/1200)**(time_period*12)-1)/(interest_r/1200))*(1+interest_r/1200)
    invested = sip_amt*time_period*12
    exp_return = round(returns_t-invested)
    with col2:
        st.metric('Total Invested', f'₹ {invested:,}',)
        st.metric('Returns', f'₹ {exp_return:,}',f'{round(exp_return*100/invested,2)}%')
        st.metric('Total Value', f'₹ {round(returns_t):,}',f'{round(returns_t/invested,2)}x ')

    #?Tab1 pie chart
    colors = ['seagreen', 'lightgreen']
    pie_data = {'Expected Returns': exp_return, 'Total Invested': invested}
    fig1 = px.pie(values=pie_data.values(), names=pie_data.keys(), labels=pie_data.keys(), title='Invested vs Returns', hole=0.6, width=500, height=500)
    fig1.update_traces(textposition='outside', textinfo='percent', marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    with col1:
        st.plotly_chart(fig1)

#! Tab2 contents:
#?Tab2 columns defined
with tab2:
    col1, col2 = st.columns(2)
    
    #?Tab2 slider controls
    with col1:
        loan_amt = st.select_slider('Principal Amount',[n for n in range(50000, 10050000, 50000)])
        interest_l = st.select_slider('Loan Interest (%)',[round(i,1) for i in np.arange(1.0, 30.1, 0.1)])
        tenure = st.slider('Tenure', 1, 30)

    #?Tab2 calculations & metric display
    emi_amt = loan_amt*(interest_l/1200)*(1+interest_l/1200)**(tenure*12)/((1+interest_l/1200)**(tenure*12)-1)
    loan_plus_int = round(emi_amt*tenure*12)
    interest_amt = loan_plus_int-loan_amt
    int_per_loan = round(interest_amt/loan_amt,2)
    with col2:
        st.metric('Monthly EMI', f'₹ {round(emi_amt):,}',)
        st.metric('Total Interest', f'₹ {interest_amt:,}',f'{round(int_per_loan*100,2)}%')
        st.metric('Total Value', f'₹ {loan_plus_int:,}',f'{int_per_loan}x')

    #?Tab2 pie chart
    colors = ['orangered', 'salmon']
    pie_data = {'Interest Amount': interest_amt, 'Principal Amount': loan_amt}
    fig2 = px.pie(values=pie_data.values(), names=pie_data.keys(), labels=pie_data.keys(), title='Principal vs Loan Interest', hole=0.6, width=500, height=500)
    fig2.update_traces(textposition='outside', textinfo='percent', marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    with col1:
        st.plotly_chart(fig2)

    #?Tab2 amortization schedule
    with col2:
            with st.expander('Loan Repayment Schedule', expanded=True):
                loan_tenure = tenure*12
                m,p,i,e,b = amort(loan_amt, interest_l, loan_tenure, emi_amt)
                data = {'Month':m, 'EMI':e, 'Principle':p, 'Interest':i, 'Balance':b}
                df = pd.DataFrame(data).set_index('Month')
                df = df.style.format({'Month':'₹{:,}', 'EMI':'₹{:,}', 'Principle':'₹{:,}', 'Interest':'₹{:,}', 'Balance':'₹{:,}'})
                st.dataframe(df)

#! Tab3 contents:
#?Tab3 variables
tenK = 10000
std_dedct = 5*tenK

#?Tab3 tax regime selection
with tab3:
    tax_regime = st.radio('Choose your Tax regime:',["Old Tax Regime","New Tax Regime"])
    col1, col2 = st.columns(2)
    with col1:
        sal = st.number_input("Enter your Salary",10*tenK,1000*tenK)
    with col2:
        emp = st.metric("Gross Salary (p.a.)", f'₹ {round(sal):,}')

    #?Tab3 exemptions & deductions
    with col1:
        st.subheader("Exemptions")
        hra = st.number_input("HRA",0,100*tenK)
        pt = st.number_input("Professional Tax",0,tenK)
        hl = st.number_input("Housing Loan Interest",0,tenK)
        gross_sal = round(sal-hra-pt-hl-std_dedct)
        gross_sal_display = st.metric("Gross Total Income (after ₹ 50000 standard deduction)",f'₹ {gross_sal:,}')
    with col2:
        st.subheader("Deductions")
        c80 = st.number_input("Section 80C (LIC, ELSS, PPF etc.)",0,100*tenK)
        ccd80 = st.number_input("Section 80CCD (NPS Employee Contribution only)",0,100*tenK)
        d80 = st.number_input("Section 80D (Medical Insurance Premium of Self & Parents)",0,100*tenK)
        net_sal = round(gross_sal-(c80 if c80<15*tenK else 15*tenK)-(ccd80 if ccd80<5*tenK else 5*tenK)-(d80 if ccd80<10*tenK else 10*tenK))
        st.metric("Net Taxable Income",f'₹ {net_sal:,}')

    #?Tab3 tax calculation on regime basis
    if tax_regime == "Old Tax Regime":
        tax5 = calc_tax(net_sal, 25, 0.05, 50, 1.25).tax_slab1()
        tax20 = calc_tax(net_sal, 50, 0.2, 100, 10).tax_slab1()
        tax30 = calc_tax(net_sal, 100, 0.3, 0, 0).tax_slab2()
        cess = calc_tax(net_sal, 0, 0, 50, 0, tax5, tax20, tax30).cess4()
        rebate = round(0 if net_sal>50*tenK else tax5)
        with st.expander('Tax Details', expanded=True):
                st.subheader(f"Up to ₹ 2.5 lakh @ 0% = ₹ 0")
                st.subheader(f"₹ 2,50,001 to ₹ 5 lakh @ 5% = ₹ {tax5:,}")
                st.subheader(f"₹ 5,00,001 to ₹ 10 lakh @ 20% = ₹ {tax20:,}")
                st.subheader(f"Over ₹ 10 lakh @ 30% = ₹ {tax30:,}")
                st.subheader(f"Cess @ 4% = ₹ {cess:,}")
                st.subheader(f"Tax Rebate = ₹ {rebate:,}")
                st.metric("Your Tax",f'₹ {round(tax5+tax20+tax30+cess-rebate):,}')
    else:
        tax5 = calc_tax(net_sal, 30, 0.05, 60, 1.5).tax_slab1()
        tax10 = calc_tax(net_sal, 60, 0.1, 90, 3).tax_slab1()
        tax15 = calc_tax(net_sal, 90, 0.15, 120, 4.5).tax_slab1()
        tax20 = calc_tax(net_sal, 120, 0.2, 150, 6).tax_slab1()
        tax30 = calc_tax(net_sal, 150, 0.3, 0, 0).tax_slab2()
        cess = calc_tax(net_sal, 0, 0, 50, 0, tax5, tax10, tax15, tax20, tax30).cess4()
        rebate = round(0 if net_sal>70*tenK else tax5+tax10)
        with st.expander('Tax Details', expanded=True):
                st.subheader(f"Up to ₹ 3 lakh @ 0% = ₹ 0")
                st.subheader(f"₹ 3,00,001 to ₹ 6 lakh @ 5% = ₹ {tax5:,}")
                st.subheader(f"₹ 6,00,001 to ₹ 9 lakh @ 10% = ₹ {tax10:,}")
                st.subheader(f"₹ 9,00,001 to ₹ 12 lakh @ 15% = ₹ {tax15:,}")
                st.subheader(f"₹ 12,00,001 to ₹ 15 lakh @ 20% = ₹ {tax20:,}")
                st.subheader(f"Over ₹ 15 lakh @ 30% = ₹ {tax30:,}")
                st.subheader(f"Cess @ 4% = ₹ {cess:,}")
                st.subheader(f"Tax Rebate = ₹ {rebate:,}")
                st.metric("Your Tax",f'₹ {round(tax5+tax10+tax15+tax20+tax30+cess-rebate):,}')

#! Tab4 contents:
#?Tab4 columns defined
with tab4:
    col1, col2 = st.columns(2)
    
    #?Tab4 slider controls
    with col1:
        inv_amt = st.select_slider('Yearly Investment',[n for n in np.arange(500, 150500, 500)])
        time_period = st.slider('Time Period (in years)', 15, 50)
        st.write('Rate of Interest: 7.1%')
        interest_r = 7.1

    #?Tab4 calculations & metric display
    returns_t = inv_amt*(((1.071**time_period)-1)/0.071)*(1.071)
    invested = inv_amt*time_period
    exp_return = round(returns_t-invested)
    with col2:
        st.metric('Invested Amount', f'₹ {invested:,}',)
        st.metric('Total Interest', f'₹ {exp_return:,}',f'{round(exp_return*100/invested,2)}%')
        st.metric('Maturity Value', f'₹ {round(returns_t):,}',f'{round(returns_t/invested,2)}x ')

    #?Tab4 pie chart
    colors = ['palevioletred', 'pink']
    pie_data = {'Expected Returns': exp_return, 'Total Invested': invested}
    fig1 = px.pie(values=pie_data.values(), names=pie_data.keys(), labels=pie_data.keys(), title='Invested vs Returns', hole=0.6, width=500, height=500)
    fig1.update_traces(textposition='outside', textinfo='percent', marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    with col1:
        st.plotly_chart(fig1)