import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import json
import urllib
import streamlit as st
import yfinance as yf

# Interactive table
def select_table(df, jscode):
    """
    Create a table with selection capability
    :param df: dataframe to select from
    :return: selected rows
    """

    gd = GridOptionsBuilder.from_dataframe(df)
    cellsytle_jscode = JsCode(jscode)
    gd.configure_columns(
        (
            "Buying Distance (%)",
        ),
        cellStyle=cellsytle_jscode,
    )
    gd.configure_pagination(enabled=True)
    gd.configure_columns(("Ticker", "Buying Distance (%)"), pinned=True)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(
        df,
        gridOptions=gridoptions,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="material",
        allow_unsafe_jscode=True,
    )

    return pd.DataFrame(grid_table["selected_rows"])

# Find the PS ratio of a stock
def get_PSratio(Symbol):

    api = "e2ddb9db079212837b432d1641354915"
    url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{Symbol}?apikey={api}"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    data = json.loads(data)

    try:
        return data[0]['priceToSalesRatioTTM']
    except Exception as e:
        return 0

# This funtion scraps each Symbol page and extract the Zacks Rank
def Zacks_Rank(Symbol):

    url = 'https://quote-feed.zacks.com/index?t=' + Symbol
    downloaded_data = urllib.request.urlopen(url)
    data = downloaded_data.read()
    data_str = data.decode()
    Z_Rank = ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]

    for Rank in Z_Rank:
        if data_str.find(Rank) != -1:
            return Rank
        
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# Get the live stock price
def stock_price(Symbol):
    stock_info = yf.Ticker(Symbol).info
    price = stock_info['currentPrice']
    return price