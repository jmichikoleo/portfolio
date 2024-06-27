#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def fetch_stock_data_from_file(ticker):
    filename = f"{ticker}_{pd.Timestamp.today().strftime('%Y-%m-%d')}.csv"
    try:
        data = pd.read_csv(filename, index_col=0)
        return data
    except FileNotFoundError:
        return None

def main():
    st.title('Stock Data Dashboard')

    ticker = st.text_input('Enter stock ticker (e.g., AAPL):')

    if st.button('Fetch Data'):
        if ticker:
            data = fetch_stock_data_from_file(ticker)
            if data is not None:
                st.write(f"### Displaying data for {ticker}")
                st.write(data)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
                fig.update_layout(title=f'{ticker} Closing Price',
                                  xaxis_title='Date',
                                  yaxis_title='Price (USD)')
                st.plotly_chart(fig)
            else:
                st.write(f"No data available for {ticker} yet. Please run the update script.")

if __name__ == '__main__':
    main()

