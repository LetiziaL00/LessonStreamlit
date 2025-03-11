import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import date
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


option = st.sidebar.selectbox("What do want to do?", ('Stock Analysis', 'Correlation Analysis'))

if option == 'Stock Analysis':
    symbol = st.sidebar.selectbox("Ticker", ['AAPL', 'TLSA', 'MSFT', 'BTC-USD'])

    start_date = st.sidebar.date_input("Start date", date.today()+pd.DateOffset(years=-1))
    end_date = st.sidebar.date_input("End date", date.today())
    stock = yf.download(symbol, start=start_date, end=end_date)

    st.write("""# Resume""")
    st.write("""Ticker:""", symbol)
    st.write('Last Close: ' + str(round(stock['Close'].values[-1,0] ,2)))
    st.write('Last Volume: ' + str(round(stock['Volume'].values[-1,0] ,2)))

    stock = stock.swaplevel(axis=1)
    stock = stock[symbol] #eliminate the ticker from columns name
    # print() # non è utile perchè non devi fare run, ma salvare e basta
    st.dataframe(stock)
    st.download_button("Press to Download", 
                        stock.to_csv().encode('utf-8'), 
                        file_name = symbol+start_date.strftime("%m%d%Y")+end_date.strftime("%m%d%Y")+".csv",
                        mime="text/csv", key='download-csv')

    st.write(""" # Close prices analysis """)
    # st.line_chart(stock.Close)
    fig = px.line(stock, y='Close')
    st.plotly_chart(fig, use_container_width=True)

    logret = np.log(stock.Close).diff().dropna()
    st.write(""" Descriptive statistics of log-returns """)
    st.dataframe(logret.describe().transpose())

    # histogram
    histret = plt.figure(figsize=(8,6))
    plt.title("Log-returns histogram")
    sns.histplot(logret, color='red', stat="density")
    st.pyplot(histret)









