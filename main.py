import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import date
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import myfun as mf


option = st.sidebar.selectbox("What do you want to do?", ('Stock Analysis', 'Correlation Analysis'))
if option == 'Stock Analysis':
    symbol = st.sidebar.selectbox("Ticker", ['AAPL', 'TLSA', 'MSFT', 'BTC-USD'])
    start_date = st.sidebar.date_input("Start date", date.today()+pd.DateOffset(years=-1))
    end_date = st.sidebar.date_input("End date", date.today())
    stock = yf.download(symbol, start=start_date, end=end_date)

    st.write(""" # Resume """)
    st.write("""Ticker: """, symbol)
    st.write('Last Close:' + str(round(stock['Close'].values[-1,0], 2)))
    st.write('Last Volume:' + str(round(stock['Volume'].values[-1,0], 2)))
    #print(stock) #it's not useful because we're not running the code

    stock = stock.swaplevel(axis=1) #column index
    stock = stock[symbol] #we eliminate the first level (ticker) of column names
    st.dataframe(stock) #show a pandas dataframe in the web application
    st.download_button("Press to Download", stock.to_csv().encode('utf-8'), file_name=symbol+start_date.strftime("%m%d%Y")+end_date.strftime("%m%d%Y")+".csv", mime="text/csv", key='download-csv')

    st.write(""" # Close prices analysis """)
    #st.line_chart(stock.Close)
    fig = px.line(stock, y='Close')
    st.plotly_chart(fig, use_container_width=True) #to adjust the size of the figure

    logret = np.log(stock.Close).diff().dropna()
    st.write("""Descriptive statistics of log-returns """)
    st.dataframe(logret.describe().transpose())

    #Histogram
    histret = plt.figure(figsize=(8,6))
    plt.title("Log-returns histogram")
    sns.histplot(logret, color='red', stat="density")
    mf.normal(logret.mean(), logret.std())
    st.pyplot(histret)

if option == 'Correlation Analysis':
    start_date = st.sidebar.date_input("Start date", date.today()+pd.DateOffset(years=-1))
    end_date = st.sidebar.date_input("End date", date.today())
    ticker_list = ['AAPL', 'MSFT', 'TSLA', 'BTC-USD']
    portfolio = st.sidebar.multiselect('Tickers', ticker_list, default = ticker_list)

    st.write(""" # Your portfolio """)
    st.markdown(portfolio)

    df = yf.download(portfolio, start=start_date, end=end_date)['Close']
    st.write("""# Close prices """)
    df = df.dropna()
    st.dataframe(df)

    ret = np.log(df).diff().dropna()
    st.write("# Correlation matrix")
    correl = ret.corr()
    correl 

    fig_corr = plt.figure()
    sns.heatmap(correl, annot=True, cmap='Reds', center=1, linewidths=0.5) #center is the highest value
    st.pyplot(fig_corr)
