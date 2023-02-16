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

st.button('Calculate Home Loan EMIs')